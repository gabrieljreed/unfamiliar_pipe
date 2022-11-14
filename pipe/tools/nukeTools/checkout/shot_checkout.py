from pipe.pipeHandlers.environment import Environment as env
from pipe.pipeHandlers.element import Element
import pipe.pipeHandlers.permissions as permissions

import PySide2.QtWidgets as QtWidgets

import os
from PySide2 import QtWidgets, QtCore

import nuke


class ShotCheckout(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.env = env()
        self.shots = self.env.get_shot_list()
        self.shots.sort()
        self.setupUI()
        self.updateUI()

    def setupUI(self):
        self.setWindowTitle("Checkout Shot")

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        self.mainLayout.addWidget(QtWidgets.QLabel("Shot:"))

        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search")
        self.searchBox.textEdited.connect(self.search)
        self.mainLayout.addWidget(self.searchBox)

        self.shotList = QtWidgets.QListWidget()
        self.shotList.setAlternatingRowColors(True)
        self.shotList.addItems(self.shots)
        self.shotList.itemDoubleClicked.connect(self.checkout)
        self.mainLayout.addWidget(self.shotList)

        self.buttonBox = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonBox)

        self.checkoutButton = QtWidgets.QPushButton("Checkout")
        self.checkoutButton.clicked.connect(self.checkout)
        self.buttonBox.addWidget(self.checkoutButton)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        self.buttonBox.addWidget(self.cancelButton)

    def updateUI(self):
        self.shotList.clear()
        self.shotList.addItems(self.shots)

    def search(self):
        """Updates the list of shots to only show the ones that match the search query"""
        searchTerm = self.searchBox.text()
        self.shotList.clear()
        self.shotList.addItems([shot for shot in self.shots if searchTerm in shot])

    def checkout(self):
        if self.shotList.currentItem() is None:
            return

        shot = self.shotList.currentItem().text()

        nukeFilePath = self.env.get_nuke_dir(shot)

        if not os.path.isdir(os.path.dirname(nukeFilePath)):
            os.makedirs(os.path.dirname(nukeFilePath))
            permissions.set_permissions(os.path.dirname(nukeFilePath))

        versionsFolder = os.path.join(os.path.dirname(nukeFilePath), ".versions")
        if not os.path.isdir(versionsFolder):
            os.makedirs(versionsFolder)
            permissions.set_permissions(versionsFolder)

        element = Element(nukeFilePath)

        if element.is_assigned():
            if element.get_assigned_user() != env().get_username():
                nuke.message("Shot is checked out by: " + element.get_assigned_user())
                return

        element.assign_user(env().get_username())
        element.write_element_file()

        # Open nuke file
        if os.path.isfile(nukeFilePath):
            nuke.scriptOpen(nukeFilePath)
        else:
            nuke.scriptSaveAs(nukeFilePath, overwrite=1)

        self.close()
