import http
import http.client
import json
import os
import pwd
import threading
from time import sleep

import maya.cmds as mc
from PySide2 import QtCore, QtWidgets


class CrashLogger(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.webhook = "https://discord.com/api/webhooks/1022539010209484830/Oaxafq6CnXuQChclGJyB80ROTF6kaVR5XDNs9OM-oq3TtuLofk1IVD3XwoS6EeEHpQMV"
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Crash Logger")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.resize(400, 300)

        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.infoLabel = QtWidgets.QLabel(
            "The information below has been detected automatically. Please review it and submit the crash report.")
        self.infoLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.infoLabel)

        self.nameLayout = QtWidgets.QHBoxLayout()
        self.artistNameLabel = QtWidgets.QLabel("Artist Name")
        self.nameLayout.addWidget(self.artistNameLabel)
        self.artistNameLineEdit = QtWidgets.QLineEdit()
        self.artistNameLineEdit.setText(self.getUsername())
        self.nameLayout.addWidget(self.artistNameLineEdit)
        self.mainLayout.addLayout(self.nameLayout)

        self.evaluationModeLayout = QtWidgets.QHBoxLayout()
        self.evaluationModeLabel = QtWidgets.QLabel("Evaluation Mode")
        self.evaluationModeLayout.addWidget(self.evaluationModeLabel)
        self.evaluationModeComboBox = QtWidgets.QComboBox()
        self.evaluationModeComboBox.addItems(["DG", "Serial", "Parallel"])
        self.evaluationModeComboBox.setCurrentText(self.getEvalMode())
        self.evaluationModeLayout.addWidget(self.evaluationModeComboBox)
        self.mainLayout.addLayout(self.evaluationModeLayout)

        self.rigsGroupBox = QtWidgets.QGroupBox("Rigs")
        self.rigsLayout = QtWidgets.QVBoxLayout(self.rigsGroupBox)
        self.maggieRigCheckBox = QtWidgets.QCheckBox("Maggie")
        self.maggieRigCheckBox.setChecked(self.isRigInScene("Maggie"))
        self.rigsLayout.addWidget(self.maggieRigCheckBox)
        self.singeRigCheckBox = QtWidgets.QCheckBox("Singe")
        self.singeRigCheckBox.setChecked(self.isRigInScene("Singe"))
        self.rigsLayout.addWidget(self.singeRigCheckBox)
        self.kellethRigCheckBox = QtWidgets.QCheckBox("Kelleth")
        self.kellethRigCheckBox.setChecked(self.isRigInScene("Kelleth"))
        self.rigsLayout.addWidget(self.kellethRigCheckBox)
        self.frogRigCheckBox = QtWidgets.QCheckBox("Frog")
        self.frogRigCheckBox.setChecked(self.isRigInScene("Frog"))
        self.rigsLayout.addWidget(self.frogRigCheckBox)
        self.dollsRigCheckBox = QtWidgets.QCheckBox("Dolls")
        self.dollsRigCheckBox.setChecked(self.isRigInScene("Dolls"))
        self.rigsLayout.addWidget(self.dollsRigCheckBox)
        self.mainLayout.addWidget(self.rigsGroupBox)

        self.layoutLoadedCheckBox = QtWidgets.QCheckBox("Layout Loaded")
        self.layoutLoadedCheckBox.setChecked(self.isRigInScene("layout"))
        self.mainLayout.addWidget(self.layoutLoadedCheckBox)

        self.additionalCommentsLabel = QtWidgets.QLabel("Additional Comments")
        self.mainLayout.addWidget(self.additionalCommentsLabel)
        self.additionalCommentsTextEdit = QtWidgets.QTextEdit()
        self.additionalCommentsTextEdit.setPlaceholderText("I was blocking...")
        self.mainLayout.addWidget(self.additionalCommentsTextEdit)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.submitButton = QtWidgets.QPushButton("Submit")
        self.submitButton.clicked.connect(self.submit)
        self.buttonLayout.addWidget(self.submitButton)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        self.buttonLayout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(self.buttonLayout)

    @staticmethod
    def getUsername():
        username = pwd.getpwuid(os.getuid())[4]
        username = username.split(" ")
        if len(username) == 3:
            username = username[0] + ' ' + username[2]
        else:
            username = username[0] + ' ' + username[1]

        return username

    @staticmethod
    def getEvalMode():
        return mc.evaluationManager(query=True, mode=True)[0].title()

    @staticmethod
    def isRigInScene(rigName):
        """Check if a rig is in the scene.
        @param rigName: Name of the rig to check for.
        @return: True if the rig is in the scene, False otherwise."""

        cameraNames = ["persp", "top", "front", "side"]
        topLevelNodes = [node for node in mc.ls(assemblies=True) if node not in cameraNames]

        found = False
        for node in topLevelNodes:
            if rigName in node:
                found = True
                break

        return found

    def submit(self):
        uploadMessage = f"""Artist Name: {self.artistNameLineEdit.text()}
Evaluation Mode: {self.evaluationModeComboBox.currentText()}
Maggie Rig: {self.maggieRigCheckBox.isChecked()}
Singe Rig: {self.singeRigCheckBox.isChecked()}
Kelleth Rig: {self.kellethRigCheckBox.isChecked()}
Frog Rig: {self.frogRigCheckBox.isChecked()}
Dolls Rig: {self.dollsRigCheckBox.isChecked()}
Layout Loaded: {self.layoutLoadedCheckBox.isChecked()}
Additional Comments: {self.additionalCommentsTextEdit.toPlainText()}"""
        print(uploadMessage)

        def threadedUpload():
            try:
                self.setEnabled(False)
                self.submitButton.setText("Uploading...")
                self.upload(uploadMessage)
                self.submitButton.setText("Submit")
                self.setEnabled(True)
            except Exception as e:
                self.submitButton.setText("Submit")
                self.setEnabled(True)
                # self.close()
                raise e

        thread = threading.Thread(target=threadedUpload)
        thread.start()

        # self.close()

    def upload(self, message):
        """Upload the given message to the server.
        @param message: The message to upload."""

        try:
            bot_message = {
                "username": "Rigging Bot",
                "content": message
            }
            host, path = parse_discord_api(self.webhook)
            connection = http.client.HTTPSConnection(host)
            connection.request('POST', path, headers={'Content-Type': 'application/json; charset=UTF-8',
                                                      'User-Agent': 'BYU Animation/1.0.0'},
                               body=json.dumps(bot_message))
            response = connection.getresponse()
            return tuple([response])
        except Exception as e:
            raise e


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


class mayaRun:
    def run(self):
        self.crashLogger = CrashLogger()
        self.crashLogger.show()
