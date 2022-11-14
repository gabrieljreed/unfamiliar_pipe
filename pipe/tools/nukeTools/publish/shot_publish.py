import os
import shutil

import nuke
import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore, QtWidgets

import pipe.pipeHandlers.permissions as permissions
from pipe.pipeHandlers.element import Element
from pipe.pipeHandlers.environment import Environment as env


class ShotPublish(QtWidgets.QMainWindow):
    """A window to publish or return a shot"""
    def __init__(self):
        super().__init__()
        self.env = env()
        self.shots = self.env.get_shot_list()
        self.shots.sort()

        try:
            self.scriptName = nuke.scriptName()
        except Exception:
            self.scriptName = None

        self.el = None

        self.setupUI()

    def setupUI(self):
        """Sets up the UI"""
        self.setWindowTitle("Publish Shot")

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        self.mainLayout.addWidget(QtWidgets.QLabel(f"Detected Shot: {self.parseFilename()}"))

        self.mainLayout.addWidget(QtWidgets.QLabel("Or, choose another shot:"))

        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search")
        self.searchBox.textEdited.connect(self.search)
        self.mainLayout.addWidget(self.searchBox)

        self.shotList = QtWidgets.QListWidget()
        self.shotList.setAlternatingRowColors(True)
        self.shotList.addItems(self.shots)
        self.shotList.itemDoubleClicked.connect(self.publish)
        self.mainLayout.addWidget(self.shotList)

        self.commentBox = QtWidgets.QTextEdit()
        self.commentBox.setPlaceholderText("Comment...")
        self.commentBox.setFixedHeight(100)
        self.mainLayout.addWidget(self.commentBox)

        self.buttonBox = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonBox)

        self.checkoutButton = QtWidgets.QPushButton("Publish")
        self.checkoutButton.clicked.connect(self.publish)
        self.buttonBox.addWidget(self.checkoutButton)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        self.buttonBox.addWidget(self.cancelButton)

    def parseFilename(self):
        """Parses the filename of the script to get the shot name"""
        if self.scriptName:
            self.shot = os.path.basename(self.scriptName).split("_main")[0]
            return self.shot
        return None

    def search(self):
        """Updates the list of shots to only show the ones that match the search query"""
        searchTerm = self.searchBox.text()
        self.shotList.clear()
        self.shotList.addItems([shot for shot in self.shots if searchTerm in shot])

    def publish(self):
        if self.shotList.currentItem():
            self.shot = self.shotList.currentItem().text()

        print("Publishing...")
        nukeFilePath = self.env.get_nuke_dir(self.shot)
        self.el = Element(nukeFilePath)

        # Save the current script
        nuke.scriptSave()

        # Get new version number
        versionNum = self.el.get_latest_version() + 1

        dirName = f"v{versionNum:04}"
        newDirPath = os.path.join(env().get_file_dir(self.el.filepath), ".versions", dirName)
        os.mkdir(newDirPath)
        newFilePath = os.path.join(newDirPath, self.el.get_file_parent_name() + self.el.get_file_ext())
        shutil.copy(self.el.filepath, newFilePath)

        permissions.set_permissions(newFilePath)

        # Update element file
        self.el.add_publish_log(self.commentBox.toPlainText())
        self.el.set_latest_version(versionNum)
        self.el.assign_user("")
        self.el.write_element_file()

        print("Publish complete!")

        self.close()
