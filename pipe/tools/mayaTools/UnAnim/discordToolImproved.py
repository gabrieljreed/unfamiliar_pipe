"""This is a heavily modified version of the original discord tool by Guilherme Trevisan found here:
https://github.com/TrevisanGMW/gt-tools/blob/release/python-scripts/gt_maya_to_discord.py

Changes include:
- Added support for multiple discord channels
- Added video compression through ffmpeg

To change the channels, edit the webhooks dictionary in the code below.
"""
import os
import threading
import json
import http
import random
from sys import platform
if platform == "linux" or platform == "linux2":
    import pwd
elif platform == "win32":
    import win32api
    import win32con
    import win32security
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as mc
import maya.utils as mu


webhooks = {
    # "modeling": "https://discord.com/api/webhooks/1023982094608760992/jA-Qc4dsjMiW2bIv0SCjfWIQ7cLPU2sYG6JOoe3lDtxereD_iZmJ1Hou1Fy4h74Y38bG",
    # "rigging": "https://discord.com/api/webhooks/1023982237986865243/ZzrEB1dd4s3Syu7Pf4ZCMhiT6f8-FCklJpmdPGVjhIiTgk8b4XayNVTS5y0ZhAY5rz8G",
    # "playblasts": "https://discord.com/api/webhooks/1024091123427319829/JJBiUopUhYgukCVD-wgENA2tx8bsDRwn7VWMXx09Sn7rgsIvRd5Dc1d9-X15GyTyfMkk",
    # "memes": "https://discord.com/api/webhooks/1023981999255470271/tzJcjAJ7DtV4f1cYPqZNUeEq8HPjnNa-7ypCSj3RtavxPoeervVR9EWSVMIsxfkS3WCp",
    "general": "https://discord.com/api/webhooks/1017080257666351144/WpIPUVYjsVJ4At2ARMla2uv9rYVzHlC0BkJLSt0rWNRuDmGxOrNnfRJRXTybBhEn8PSy",
    "memes": "https://discord.com/api/webhooks/1018918495590830151/ANHb9lismw1276JvPgG1ZTT7mr2OWdKeDmR-_Apt96jqOGumtiOi5PY0AlptCNVXA-r2",
    "stuff": "https://discord.com/api/webhooks/1022539010209484830/Oaxafq6CnXuQChclGJyB80ROTF6kaVR5XDNs9OM-oq3TtuLofk1IVD3XwoS6EeEHpQMV",
}

signatures = [
    "via Maya",
    "sent from my Samsung Smart Fridge",
    "sent from my Samsung Smart Toilet",
    "via smoke signals",
    "via Morse code",
    "sent by carrier pigeon",
    "translated from ancient metal plates",
    "via the power of the sun",
    "live from Taco Bell",
    "from ur moms house",
]


class MayaToDiscordWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self):
        parent = self.getMayaWindow()

        self.channels = webhooks  # TODO: Fix this somehow

        super(MayaToDiscordWindow, self).__init__(parent)
        self.setWindowTitle('Maya to Discord')
        # self.setWindowIcon(QIcon(icon_image))
        self.setMinimumSize(300, 500)
        self.resize(300, 500)

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # TODO: Add a way for the UI to remember the last channel used (PER USER)

        self.icon_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, os.pardir,
                         "icons", "discordIcons"))

        self.build_gui()

        self.webhook_error_message = 'Webhook is invalid. Please, check your settings.'

    def build_gui(self):
        self.setWindowIcon(QtGui.QIcon(os.path.normpath(os.path.join(self.icon_path, "discord.png"))))

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setNativeMenuBar(False)

        self.settingsMenu = self.menu_bar.addMenu('Settings')
        self.settingsMenu.addAction('Settings', self.openSettings)

        self.helpMenu = self.menu_bar.addMenu('Help')
        self.helpMenu.addAction('Help', self.openHelp)
        self.helpMenu.addAction('About', self.openAbout)

        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Add a spacer
        spacer = QtWidgets.QWidget()
        # spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding)
        spacer.setFixedHeight(15)
        self.main_layout.addWidget(spacer)

        self.input_box = QtWidgets.QPlainTextEdit(self)
        self.input_box.setPlaceholderText('Enter message here')
        self.input_box.setMinimumHeight(50)
        self.input_box.setMaximumHeight(50)
        self.main_layout.addWidget(self.input_box)

        self.main_layout.addWidget(QHLine())

        self.channel_label = QtWidgets.QLabel('Channel')
        self.channel_label.setFixedHeight(20)
        self.main_layout.addWidget(self.channel_label)
        self.channel_combo_box = QtWidgets.QComboBox(self)
        self.channel_combo_box.addItems(self.channels.keys())
        self.main_layout.addWidget(self.channel_combo_box)
        self.main_layout.addWidget(QHLine())

        self.send_text_button = QtWidgets.QToolButton()
        self.send_text_button.setText('Send Text')
        self.send_text_button.setIcon(QtGui.QIcon(os.path.join(self.icon_path, 'text.png')))
        self.send_text_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.send_text_button.setStyleSheet(
            "QToolButton::hover { background-color: #2f3136; } QToolButton { background-color: #23272a; border: 1px solid #2f3136; border-radius: 4px; }")
        self.send_text_button.clicked.connect(self.send_message)
        self.main_layout.addWidget(self.send_text_button)

        self.main_layout.addWidget(QHLine())

        self.send_screenshot_button = QtWidgets.QToolButton()
        self.send_screenshot_button.setText('Send Screenshot')
        self.send_screenshot_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.send_screenshot_button.setIcon(QtGui.QIcon(os.path.join(self.icon_path, 'desktop.png')))
        self.send_screenshot_button.setStyleSheet(
            "QToolButton::hover { background-color: #2f3136; } QToolButton { background-color: #23272a; border: 1px solid #2f3136; border-radius: 4px; }")
        self.send_screenshot_button.clicked.connect(self.send_desktop_screenshot)
        self.main_layout.addWidget(self.send_screenshot_button)

        self.send_maya_screenshot_button = QtWidgets.QToolButton()
        self.send_maya_screenshot_button.setText("Send Maya Screenshot")
        self.send_maya_screenshot_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.send_maya_screenshot_button.setIcon(QtGui.QIcon(os.path.join(self.icon_path, 'maya_window.png')))
        self.send_maya_screenshot_button.setStyleSheet(
            "QToolButton::hover { background-color: #2f3136; } QToolButton { background-color: #23272a; border: 1px solid #2f3136; border-radius: 4px; }")
        self.send_maya_screenshot_button.clicked.connect(self.send_maya_screenshot)
        self.main_layout.addWidget(self.send_maya_screenshot_button)

        self.send_viewport_screenshot_button = QtWidgets.QToolButton()
        self.send_viewport_screenshot_button.setText('Send Viewport Screenshot')
        self.send_viewport_screenshot_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.send_viewport_screenshot_button.setIcon(
            QtGui.QIcon(os.path.join(self.icon_path, 'maya_window.png')))  # FIXME: Where is this icon?
        self.send_viewport_screenshot_button.setStyleSheet(
            "QToolButton::hover { background-color: #2f3136; } QToolButton { background-color: #23272a; border: 1px solid #2f3136; border-radius: 4px; }")
        self.send_viewport_screenshot_button.clicked.connect(self.send_viewport_screenshot)
        self.main_layout.addWidget(self.send_viewport_screenshot_button)

        self.main_layout.addWidget(QHLine())

        self.send_playblast_button = QtWidgets.QToolButton()
        self.send_playblast_button.setText('Send Playblast')
        self.send_playblast_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.send_playblast_button.setIcon(QtGui.QIcon(os.path.join(self.icon_path, 'playblast.png')))
        self.send_playblast_button.setStyleSheet(
            "QToolButton::hover { background-color: #2f3136; } QToolButton { background-color: #23272a; border: 1px solid #2f3136; border-radius: 4px; }")
        self.send_playblast_button.clicked.connect(self.send_playblast)
        self.main_layout.addWidget(self.send_playblast_button)

        self.send_fbx_button = QtWidgets.QToolButton()
        self.send_fbx_button.setText('Send FBX')
        self.send_fbx_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.send_fbx_button.setIcon(QtGui.QIcon(os.path.join(self.icon_path, 'fbx.png')))
        self.send_fbx_button.setStyleSheet(
            "QToolButton::hover { background-color: #2f3136; } QToolButton { background-color: #23272a; border: 1px solid #2f3136; border-radius: 4px; }")
        self.send_fbx_button.clicked.connect(self.send_fbx)
        self.main_layout.addWidget(self.send_fbx_button)

    def getMayaWindow(self):
        # Get Maya window
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        if ptr is not None:
            return wrapInstance(int(ptr), QtWidgets.QWidget)

    def openSettings(self):
        print('Open Settings')

    def openHelp(self):
        print('Open Help')

    def openAbout(self):
        print('Open About')

    def send_message(self):
        """ Attempts to send the message only (no images/videos) using current settings """
        currentWebhook = self.channels[self.channel_combo_box.currentText()]
        print(currentWebhook)

        # # Validate the webhook
        # if not self._checkWebhookValidity(currentWebhook):
        #     mc.warning('Invalid webhook, please contact Gabe')
        #     return

        message = self.input_box.toPlainText()
        if message.strip() == '':
            mc.warning('Please enter a message to send.')
            return

        # Send the message
        def threadedUpload():
            try:
                mu.executeDeferred(self.setButtonsEnabled, False)
                response = self.postDiscordMessage(self.getUsername(), message, currentWebhook)
                mu.executeDeferred(self.setButtonsEnabled, True)
            except Exception as e:
                mc.warning('Error sending message: {}'.format(e))
                return

        thread = threading.Thread(target=threadedUpload)
        thread.start()


    def send_desktop_screenshot(self):
        print('Send Desktop Screenshot')

    def send_maya_screenshot(self):
        print('Send Maya Screenshot')

    def send_viewport_screenshot(self):
        print('Send Viewport Screenshot')

    def send_playblast(self):
        print('Send Playblast')

    def send_fbx(self):
        print('Send FBX')

    def _checkWebhookValidity(self, webhook):
        """ Checks the validity of the webhook """
        successCodes = [200, 201, 203, 204, 205, 206]
        try:
            import http
            host, path = self.parse_discord_api(webhook)
            connection = http.client.HTTPSConnection(host)
            connection.request('GET', '/' + path, headers={"Content-type": "application/json; charset=utf-8", 
                               "User-Agent": "BYUAnimation"},)
            response = connection.getresponse()
            if response.status in successCodes:
                return True
            else:
                return False

        except Exception as e:
            print("Error checking webhook validity: {}".format(e))
            return False

    @staticmethod
    def parse_discord_api(discord_webhook_full_path):
        """ Parses and returns two strings to be used with HTTPSConnection instead of Http()
            
        Args:
            discord_webhook_full_path (str): Discord Webhook (Full Path)

        Returns:
            discord_api_host (str): Only the host used for discord's api
            discord_api_repo (str): The rest of the path used to describe the webhook
        """
        path_elements = discord_webhook_full_path.replace('https://', '').replace('http://', '').split('/')
        repo = ''
        if len(path_elements) == 1:
            raise Exception('Failed to parse Discord Webhook path.')
        else:
            host = path_elements[0]
            for path_part in path_elements:
                if path_part != host:
                    repo += '/' + path_part
            return host, repo

    def setButtonsEnabled(self, enabled):
        """Sets all buttons to enabled or disabled
        @param enabled: True to enable, False to disable"""
        self.send_message_button.setEnabled(enabled)
        self.send_desktop_screenshot_button.setEnabled(enabled)
        self.send_maya_screenshot_button.setEnabled(enabled)
        self.send_viewport_screenshot_button.setEnabled(enabled)
        self.send_playblast_button.setEnabled(enabled)
        self.send_fbx_button.setEnabled(enabled)

    def postDiscordMessage(self, username, message, webhook):
        botMessage = {
            "username": username,
            "content": message
        }

        host, path = self.parse_discord_api(webhook)
        connection = http.client.HTTPSConnection(host)
        connection.request('POST', path, headers={"Content-type": "application/json; charset=utf-8",
                           "User-Agent": "BYUAnimation"}, body=json.dumps(botMessage))
        response = connection.getresponse()
        return tuple([response])

    def getUsername(self):
        username = pwd.getpwuid(os.getuid())[4]
        username = username.split(" ")
        if len(username) == 3:
            username = username[0] + ' ' + username[2]
        else:
            username = username[0] + ' ' + username[1]
        # Get a random entry in the list of signatures
        signature = random.choice(signatures)
        return "{} ({})".format(username, signature)


class QHLine(QtWidgets.QFrame):
    """Renders a horizontal line"""

    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
