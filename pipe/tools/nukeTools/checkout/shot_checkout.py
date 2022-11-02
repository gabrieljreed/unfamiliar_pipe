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
            # FIXME: This doesn't seem to be getting triggered properly
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
        nuke.message("Shot checked out by: " + env().get_username())

        element.assign_user(env().get_username())
        element.write_element_file()

        # Open nuke file
        # TODO: Open nuke file


class ShotCheckoutOld:
    """This class holds required functions to check out shots in Nuke"""

    def __init__(self):
        # Get shot list
        self.shot_list = env().get_shot_list()

    def checkout(self):
        """Starts the gui for checking out shots"""
        # Open gui to select shot file
        self.filePath = nuke.getFilename('Select a shot to checkout', '*.txt *.xml', default=env().get_shot_dir())
        print(self.filePath)
        QtWidgets.QMessageBox.information(None, "Shot Checkout", self.filePath)

    def results(self, value):
        """Called after the user interacts with the gui"""
        print("Selected shot: " + value[0])
        # Get the hip directory
        hip_dir = env().get_hip_dir(value[0])
        # Access the respective .element file
        el = Element(hip_dir)
        # Check if the .hip file is already assigned
        if el.is_assigned():
            # If the .hip is already assigned, check if it is by the same user.
            if (el.get_assigned_user() != env().get_username()):
                # If not, decline the users request
                hou.ui.displayMessage("Shot is checked out by: " + el.get_assigned_user())
                # Reopen the checkout menu
                self.checkout()
                return

        # If the user is the assigned user, or there is no assigned user, assign
        # the user to the .elemnet file
        el.assign_user(env().get_username())
        # Write the .element file to disk
        el.write_element_file()
        # open the .hip file
        hou.hipFile.load(hip_dir)
