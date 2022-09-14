import os
from functools import partial

import maya.cmds as mc

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


RIG_PATH = "/groups/unfamiliar/anim_pipeline/production/rigs"

detailsWidget = None


def getPreviousRig():
    rigs = os.listdir(RIG_PATH)
    # Ask user what rig they want to import
    dialog = QDialog()
    dialog.setWindowTitle("Reference previous version of Rig")
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlags(Qt.WindowCloseButtonHint)
    dialog.setWindowFlags(Qt.WindowMinimizeButtonHint)
    dialog.setWindowFlags(Qt.WindowMaximizeButtonHint)
    dialog.setWindowFlags(Qt.WindowContextHelpButtonHint)
    dialog.setWindowFlags(Qt.WindowFullscreenButtonHint)
    dialog.setWindowFlags(Qt.WindowShadeButtonHint)
    dialog.setWindowFlags(Qt.WindowTransparentForInput)
    dialog.setWindowFlags(Qt.WindowOverridesSystemGestures)
    dialog.setWindowFlags(Qt.WindowDoesNotAcceptFocus)

    dialog.resize(400, 100)

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    label = QLabel("Select a rig to reference")
    layout.addWidget(label)

    combo = QComboBox()
    combo.addItems(rigs)
    layout.addWidget(combo)

    button = QPushButton("Select")
    layout.addWidget(button)

    button.clicked.connect(dialog.accept)

    if not dialog.exec_():
        return

    rig = combo.currentText()
    versionsPath = os.path.join(RIG_PATH, rig, "versions")

    if not os.path.isdir(versionsPath):
        QMessageBox.warning(None, "No previous versions", "No previous versions of this rig exist")
        return
    
    versions = os.listdir(versionsPath)
    versions.sort(reverse=True)
    
    # Read in the versions.txt file if it exists
    versionsInfo = None
    if os.path.exists(os.path.join(versionsPath, "version_list.txt")):
        with open(os.path.join(versionsPath, "version_list.txt"), "r") as f:
            versionsInfo = f.read().splitlines()

    # Remove any .txt files from versions 
    for version in versions:
        if version.endswith(".txt"):
            versions.remove(version)

    # Launch dialog to select version
    dialog = QDialog()
    dialog.setWindowTitle("Reference previous version of Rig")
    dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
    dialog.setWindowFlags(Qt.WindowCloseButtonHint)
    dialog.setWindowFlags(Qt.WindowMinimizeButtonHint)
    dialog.setWindowFlags(Qt.WindowMaximizeButtonHint)
    dialog.setWindowFlags(Qt.WindowContextHelpButtonHint)
    dialog.setWindowFlags(Qt.WindowFullscreenButtonHint)
    dialog.setWindowFlags(Qt.WindowShadeButtonHint)
    dialog.setWindowFlags(Qt.WindowTransparentForInput)
    dialog.setWindowFlags(Qt.WindowOverridesSystemGestures)
    dialog.setWindowFlags(Qt.WindowDoesNotAcceptFocus)

    dialog.resize(400, 100)

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    label = QLabel("Select a version to reference")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    hBox = QHBoxLayout()
    layout.addLayout(hBox)

    global detailsWidget

    versionListWidget = QListWidget()
    versionListWidget.itemClicked.connect(partial(setupVersionDetails, versionListWidget, versionsInfo))
    hBox.addWidget(versionListWidget)
    for version in versions:
        versionListWidget.addItem(version)
    
    if versionsInfo:
        setupVersionDetails(versionListWidget, versionsInfo)
        hBox.addWidget(detailsWidget)

    button = QPushButton("Reference")
    layout.addWidget(button)

    button.clicked.connect(dialog.accept)

    if not dialog.exec_():
        return

    version = versionListWidget.currentItem().text()
    versionPath = os.path.join(versionsPath, version)
    if not os.path.isfile(versionPath):
        QMessageBox.warning(None, "Unable to reference", "Unable to reference version {}".format(version))
        return

    mc.file(versionPath, r=True, namespace=rig)


def setupVersionDetails(versionListWidget, versionsInfo, *args):
    global detailsWidget

    detailsWidget = QWidget()
    detailsWidget.setFixedWidth(175)
    detailsLayout = QVBoxLayout()
    detailsWidget.setLayout(detailsLayout)

    if versionListWidget.currentItem() is None or versionsInfo is None:
        label = QLabel("Select a version to see details")
        detailsLayout.addWidget(label)
        return detailsWidget

    print("Setup version details")

    currentInfo = None
    for info in versionsInfo:
        split = info.split(" ")
        # Remove any empty strings or "-"s
        split = [i for i in split if i != "" and i != "-"]
        # Search for the current version
        if split[0] in versionListWidget.currentItem().text():
            currentInfo = split
            break

    if currentInfo is None:
        label = QLabel("No version info found")
        detailsLayout.addWidget(label)
        return detailsWidget

    version = currentInfo[0]
    versionLabel = QLabel()
    versionLabel.setText(version)
    detailsLayout.addWidget(versionLabel)

    date = currentInfo[1]
    dateLabel = QLabel()
    dateLabel.setText(date)
    detailsLayout.addWidget(dateLabel)

    time = currentInfo[2]
    timeLabel = QLabel()
    timeLabel.setText(time)
    detailsLayout.addWidget(timeLabel)

    description = " ".join(currentInfo[3:])
    descriptionLabel = QLabel()
    descriptionLabel.setText(description)
    detailsLayout.addWidget(descriptionLabel)

    print("Finished setting up version details")

    return detailsWidget


class mayaRun:
    def run(self):
        getPreviousRig()