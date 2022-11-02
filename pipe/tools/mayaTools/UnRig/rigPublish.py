import os
from datetime import datetime
from functools import partial
import shutil

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import maya.cmds as mc
import maya.mel as mm

import pipe.pipeHandlers.permissions as permissions


# RIG_PATH = "/groups/unfamiliar/anim_pipeline/production/rigs"
RIG_PATH = os.path.join(os.environ["MEDIA_PROJECT_DIR"], "production", "rigs")


class RigPublish(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.rigs = []

        self.setupUI()
        self.updateUI()

    def setupUI(self):
        self.setWindowTitle("Publish Rig")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(Qt.WindowFullscreenButtonHint)
        self.setWindowFlags(Qt.WindowShadeButtonHint)
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.setWindowFlags(Qt.WindowTransparentForInput)
        self.setWindowFlags(Qt.WindowOverridesSystemGestures)
        self.setWindowFlags(Qt.WindowDoesNotAcceptFocus)

        self.resize(250, 100)

        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        self.radioButtonLayout = QHBoxLayout()

        self.characterRadioButton = QRadioButton("Character")
        self.characterRadioButton.setChecked(True)
        self.characterRadioButton.toggled.connect(self.updateUI)
        self.radioButtonLayout.addWidget(self.characterRadioButton)

        self.propRadioButton = QRadioButton("Prop")
        self.propRadioButton.toggled.connect(self.updateUI)
        self.radioButtonLayout.addWidget(self.propRadioButton)

        self.mainLayout.addLayout(self.radioButtonLayout)

        self.directionsLabel = QLabel("Select a rig to publish")
        self.mainLayout.addWidget(self.directionsLabel)

        self.rigListWidget = QListWidget()
        self.rigListWidget.addItems(self.rigs)
        self.rigListWidget.setAlternatingRowColors(True)
        self.mainLayout.addWidget(self.rigListWidget)

        self.newRigButton = QPushButton("Create New Character Rig")
        self.mainLayout.addWidget(self.newRigButton)
        self.newRigButton.clicked.connect(self.createNewRig)

        self.commitMessageLabel = QLabel("Commit Message")
        self.mainLayout.addWidget(self.commitMessageLabel)

        self.commitMessageLineEdit = QLineEdit()
        self.commitMessageLineEdit.setPlaceholderText("Made everything not broken")
        self.mainLayout.addWidget(self.commitMessageLineEdit)

        self.publishButton = QPushButton("Publish")
        self.mainLayout.addWidget(self.publishButton)
        self.publishButton.clicked.connect(partial(self.publishRig, False, ""))

    def updateUI(self):
        self.getRigs()
        self.rigListWidget.clear()
        self.rigListWidget.addItems(self.rigs)

        self.newRigButton.setText(f"Create New {self.getRigType().title()} Rig")

    def getRigs(self):
        rigType = self.getRigType()
        if rigType == "character":
            self.rigs = os.listdir(RIG_PATH)
            if "props" in self.rigs:
                self.rigs.remove("props")
        elif rigType == "prop":
            self.rigs = os.listdir(os.path.join(RIG_PATH, "props"))

    def getRigType(self):
        if self.characterRadioButton.isChecked():
            return "character"
        elif self.propRadioButton.isChecked():
            return "prop"

    def createNewRig(self):
        # Ask the user what to name the new rig
        rigName, ok = QInputDialog.getText(self, "New Rig Name", "Enter a name for the new rig")
        if ok:
            if not rigName.endswith("_main"):
                rigName = f"{rigName}_main"
            print(f"Creating new rig: {rigName}")
            # Get the folder path
            rigType = self.getRigType()
            if rigType == "character":
                rigPath = os.path.join(RIG_PATH, rigName)
            elif rigType == "prop":
                rigPath = os.path.join(RIG_PATH, "props", rigName)

            if os.path.exists(rigPath):
                QMessageBox.warning(self, "Rig Already Exists", f"The rig {rigName} already exists")
                return

            # Create the folder
            print("Creating character folder")
            try:
                os.mkdir(rigPath)
            except Exception as e:
                print(f"Unable to create folder: {rigPath}")
                print(e)
                return

            self.updateUI()

            messageBox = QMessageBox()
            messageBox.setWindowTitle("Rig Created")
            messageBox.setText(f"Rig {rigName} created successfully")
            publishButton = messageBox.addButton("Publish", QMessageBox.AcceptRole)
            publishButton.clicked.connect(partial(self.publishRig, True, rigName))
            messageBox.exec_()

    def publishRig(self, new=False, name="", *args):
        if not new:
            if self.rigListWidget.currentItem() is None:
                QMessageBox.warning(self, "No Rig Selected", "Please select a rig to publish")
                return
            rigName = self.rigListWidget.currentItem().text()

            if self.commitMessageLineEdit.text().strip() == "":
                QMessageBox.warning(self, "No Commit Message", "Please enter a commit message")
                return
            commitMessage = self.commitMessageLineEdit.text().strip()
        else:
            rigName = name
            commitMessage = f"Created new rig: {rigName}"

        rigType = self.getRigType()

        # Get the folder path
        if rigType == "character":
            rigPath = os.path.join(RIG_PATH, rigName)
        elif rigType == "prop":
            rigPath = os.path.join(RIG_PATH, "props", rigName)
        else:
            raise ValueError("Invalid rig type")

        versionsFolder = os.path.join(rigPath, "versions")
        if not os.path.exists(versionsFolder):
            os.mkdir(versionsFolder)
            permissions.set_permissions(versionsFolder)

        # Edit the versions file
        versionsFile = None
        for file in os.listdir(versionsFolder):
            if file.endswith(".txt"):
                versionsFile = os.path.join(versionsFolder, file)
                break

        # If the versions file doesn't exist, create it
        if versionsFile is None:
            print("Creating new versions file...")
            versionsFile = os.path.join(versionsFolder, "versions.txt")
            f = open(versionsFile, "w")
            f.close()

        # Add the new version to the versions file
        now = datetime.now()
        date = now.strftime("%m/%d/%Y")
        time = now.strftime("%H:%M")
        # This doesn't need to be +1 because the versions file is in the folder
        versionNumber = "{0:03d}".format(len(os.listdir(versionsFolder)))
        print(f"Version Number: {versionNumber}")
        versionMessage = f"v{versionNumber} {date} {time} - {commitMessage}\n"

        with open(versionsFile, "a") as f:
            f.write(versionMessage)

        # Move the now-old rig to the versions folder if it exists
        oldMainFile = os.path.join(rigPath, f"{rigName}_main.mb")
        if os.path.exists(oldMainFile):
            newFile = os.path.join(versionsFolder, f"{rigName}_v{versionNumber}.mb")
            os.rename(oldMainFile, os.path.join(versionsFolder, f"{rigName}_main_v{versionNumber}.mb"))

        # Save the new rig
        rigFile = os.path.join(rigPath, f"{rigName}_main.mb")
        print(f"Saving {rigFile}...")
        mc.file(rigFile, exportAll=True, type="mayaBinary", force=True, constructionHistory=True, 
                preserveReferences=True)

        # Set the permissions on the new rig
        print("Setting permissions on new rig...")
        permissions.set_permissions(rigPath)

        messageBox = QMessageBox(self)
        messageBox.setText(f"Rig {rigName} has been published")
        messageBox.setWindowTitle("Rig Published")
        openOutputFolderButton = messageBox.addButton("Open Output Folder", QMessageBox.AcceptRole)
        openOutputFolderButton.clicked.connect(lambda: os.system('xdg-open "%s"' % os.path.dirname(rigFile)))
        openOutputFolderButton.clicked.connect(self.close)
        closeButton = messageBox.addButton("Close", QMessageBox.RejectRole)
        closeButton.clicked.connect(self.close)
        messageBox.exec_()


def publish():
    rigs = os.listdir(RIG_PATH)
    # Ask user what rig they are publishing
    dialog = QDialog()
    dialog.setWindowTitle("Publish Rig")
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlags(Qt.WindowCloseButtonHint)
    dialog.setWindowFlags(Qt.WindowMinimizeButtonHint)
    dialog.setWindowFlags(Qt.WindowMaximizeButtonHint)
    dialog.setWindowFlags(Qt.WindowContextHelpButtonHint)
    dialog.setWindowFlags(Qt.WindowFullscreenButtonHint)
    dialog.setWindowFlags(Qt.WindowShadeButtonHint)
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlags(Qt.WindowStaysOnBottomHint)
    dialog.setWindowFlags(Qt.WindowTransparentForInput)
    dialog.setWindowFlags(Qt.WindowOverridesSystemGestures)
    dialog.setWindowFlags(Qt.WindowDoesNotAcceptFocus)

    dialog.resize(250, 100)

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    rigTypeLabel = QLabel("Rig Type")
    layout.addWidget(rigTypeLabel)

    characterRadioButton = QRadioButton("Character")
    characterRadioButton.setChecked(True)
    layout.addWidget(characterRadioButton)

    propRadioButton = QRadioButton("Prop")
    layout.addWidget(propRadioButton)

    label = QLabel("Select a rig to publish")
    layout.addWidget(label)

    combo = QComboBox()
    combo.addItems(rigs)
    layout.addWidget(combo)

    button = QPushButton("Next")
    layout.addWidget(button)

    button.clicked.connect(dialog.accept)

    if not dialog.exec_():
        return

    rig = combo.currentText()

    # Ask user for a commit message
    commitMessageDialog = QDialog()
    commitMessageDialog.setWindowTitle("Commit Message")

    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlags(Qt.WindowCloseButtonHint)
    dialog.setWindowFlags(Qt.WindowMinimizeButtonHint)
    dialog.setWindowFlags(Qt.WindowMaximizeButtonHint)
    dialog.setWindowFlags(Qt.WindowContextHelpButtonHint)
    dialog.setWindowFlags(Qt.WindowFullscreenButtonHint)
    dialog.setWindowFlags(Qt.WindowShadeButtonHint)
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlags(Qt.WindowStaysOnBottomHint)
    dialog.setWindowFlags(Qt.WindowTransparentForInput)
    dialog.setWindowFlags(Qt.WindowOverridesSystemGestures)
    dialog.setWindowFlags(Qt.WindowDoesNotAcceptFocus)

    commitMessageDialog.resize(250, 100)

    commitMessageLayout = QVBoxLayout()
    commitMessageDialog.setLayout(commitMessageLayout)

    commitMessageLabel = QLabel("Enter a commit message")
    commitMessageLayout.addWidget(commitMessageLabel)

    commitMessageLineEdit = QLineEdit()
    commitMessageLayout.addWidget(commitMessageLineEdit)
    commitMessageLineEdit.returnPressed.connect(commitMessageDialog.accept)

    commitMessageButton = QPushButton("Publish")
    commitMessageLayout.addWidget(commitMessageButton)

    commitMessageButton.clicked.connect(commitMessageDialog.accept)

    if not commitMessageDialog.exec_():
        return

    commitMessage = commitMessageLineEdit.text()

    # Get the folder path
    rigFolder = os.path.join(RIG_PATH, rig)
    versionsFolder = os.path.join(rigFolder, "versions")
    if not os.path.exists(versionsFolder):
        os.makedirs(versionsFolder)

    # Edit the versions file
    versionsFile = None
    for file in os.listdir(versionsFolder):
        if file.endswith("version_list.txt"):
            versionsFile = file
            break

    # If the versions file doesn't exist, create it
    if versionsFile is None:
        f = open(os.path.join(versionsFolder, "version_list.txt"), "w")
        f.close()
        versionsFile = os.path.join(versionsFolder, "version_list.txt")

    # Add the new version to the versions file
    now = datetime.now()
    date = now.strftime("%Y/%m/%d")
    time = now.strftime("%H:%M")
    versionNumber = "{0:03d}".format(len(os.listdir(versionsFolder)))
    print("versionNumber: {}".format(versionNumber))
    versionMessage = "v{} {} {} - {}\n".format(versionNumber, date, time, commitMessage)

    with open(os.path.join(versionsFolder, versionsFile), "a") as f:
        f.write(versionMessage)

    # Move the now old rig to the versions folder if it exists
    oldMainFile = os.path.join(rigFolder, "{}_main.mb".format(rig))
    if os.path.exists(oldMainFile):
        newFile = os.path.join(versionsFolder, "{}_v{}.mb".format(rig, versionNumber))
        os.rename(oldMainFile, newFile)

    rigFile = os.path.join(rigFolder, "{}_main.mb".format(rig))
    mc.file(rigFile, exportAll=True, type="mayaBinary", force=True, constructionHistory=True, preserveReferences=True)

    # Change permissions
    permissions.set_permissions(rigFolder)

    successMessage = "// Result: " + rigFile.replace("\\", "/")
    mm.eval('print("' + successMessage + '")')

    messageBox = QMessageBox(self)
    messageBox.setText("Playblast exported successfully!")
    openOutputFolderButton = messageBox.addButton("Open Output Folder", QMessageBox.AcceptRole)
    openOutputFolderButton.clicked.connect(lambda: os.system('xdg-open "%s"' % os.path.dirname(rigFolder)))
    openOutputFolderButton.clicked.connect(self.close)
    closeButton = messageBox.addButton("Close", QMessageBox.RejectRole)
    messageBox.exec_()


class mayaRun:
    def run(self):
        rigPublishDialog = RigPublish()
        rigPublishDialog.exec_()
