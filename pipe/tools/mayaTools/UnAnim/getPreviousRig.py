import os
from functools import partial

import maya.cmds as mc

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


RIG_PATH = "/groups/unfamiliar/anim_pipeline/production/rigs"

detailsWidget = None


class GetPreviousRigUI:
    def __init__(self):
        self.detailsWidget = None
        self.versionListWidget = None
        self.hBox = None
        self.versionLabel = None
        self.dateLabel = None
        self.timeLabel = None
        self.descriptionLabel = None

        self.detailsWidget = QWidget()
        self.detailsWidget.setObjectName("detailsWidget")
        self.detailsWidget.setMinimumWidth(250)
        detailsLayout = QVBoxLayout()
        self.detailsWidget.setLayout(detailsLayout)

        self.versionLabel = QLabel()
        self.versionLabel.setObjectName("versionLabel")
        detailsLayout.addWidget(self.versionLabel)

        self.dateLabel = QLabel()
        self.dateLabel.setObjectName("dateLabel")
        detailsLayout.addWidget(self.dateLabel)

        self.timeLabel = QLabel()
        self.timeLabel.setObjectName("timeLabel")
        detailsLayout.addWidget(self.timeLabel)

        self.descriptionLabel = QLabel()
        self.descriptionLabel.setObjectName("descriptionLabel")
        detailsLayout.addWidget(self.descriptionLabel)

    def getPreviousRig(self):
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

        self.hBox = QHBoxLayout()
        layout.addLayout(self.hBox)

        self.versionListWidget = QListWidget()
        # self.versionListWidget.itemClicked.connect(partial(self.setupVersionDetails, versionsInfo))
        self.versionListWidget.itemClicked.connect(partial(self.updateUI, versionsInfo))
        self.hBox.addWidget(self.versionListWidget)
        for version in versions:
            self.versionListWidget.addItem(version)
        
        if versionsInfo:
            # self.setupVersionDetails(self.versionListWidget, versionsInfo)
            self.updateUI(versionsInfo)
            self.hBox.addWidget(self.detailsWidget)

        button = QPushButton("Reference")
        layout.addWidget(button)

        button.clicked.connect(dialog.accept)

        if not dialog.exec_():
            return

        version = self.versionListWidget.currentItem().text()
        versionPath = os.path.join(versionsPath, version)
        if not os.path.isfile(versionPath):
            QMessageBox.warning(None, "Unable to reference", "Unable to reference version {}".format(version))
            return

        mc.file(versionPath, r=True, namespace=rig)


    def setupVersionDetails(self, *args):
        self.detailsWidget = QWidget()
        self.detailsWidget.setObjectName("detailsWidget")
        self.detailsWidget.setFixedWidth(175)
        detailsLayout = QVBoxLayout()
        self.detailsWidget.setLayout(detailsLayout)

        self.versionLabel = QLabel()
        self.versionLabel.setObjectName("versionLabel")
        detailsLayout.addWidget(self.versionLabel)

        self.dateLabel = QLabel()
        self.dateLabel.setObjectName("dateLabel")
        detailsLayout.addWidget(self.dateLabel)

        self.timeLabel = QLabel()
        self.timeLabel.setObjectName("timeLabel")
        detailsLayout.addWidget(self.timeLabel)

        self.descriptionLabel = QLabel()
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.descriptionLabel.setWordWrap(True)
        detailsLayout.addWidget(self.descriptionLabel)

    def updateUI(self, versionsInfo, *args):
        """Update the UI with the version details
        @param versionsInfo: string containing version info read from versions_list.txt"""
        if self.versionListWidget.currentItem() is None or versionsInfo is None:
            self.versionLabel.setText("Select a version to see details")
            return 

        currentInfo = None
        for info in versionsInfo:
            split = info.split(" ")
            # Remove any empty strings or "-"s
            split = [i for i in split if i != "" and i != "-"]
            # Search for the current version
            if split[0] in self.versionListWidget.currentItem().text():
                currentInfo = split
                break

        if currentInfo is None:
            self.versionLabel.setText("No version info found")
            return 

        version = currentInfo[0]
        self.versionLabel.setText(version)

        date = currentInfo[1]
        self.dateLabel.setText(date)

        time = currentInfo[2]
        self.timeLabel.setText(time)

        description = " ".join(currentInfo[3:])
        self.descriptionLabel.setText(description)
        self.descriptionLabel.setToolTip(description)
