import os
from datetime import datetime
import shutil

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import maya.cmds as mc
import maya.mel as mm


RIG_PATH = "/groups/unfamiliar/anim_pipeline/production/rigs"

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
    for root, dirs, files in os.walk(rigFolder):
        for file in files:
            try:
                os.chmod(os.path.join(root, file), 0o777)
            except Exception as e:
                print("Unable to change permissions on file: {}".format(os.path.join(root, file)))
    
    successMessage = "// Result: " + rigFile.replace("\\", "/")
    mm.eval('print("' + successMessage + '")')


class mayaRun:
    def run(self):
        publish()
