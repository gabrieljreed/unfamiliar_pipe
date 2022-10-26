import os

import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import maya.cmds as mc

import pipe.pipeHandlers.environment as env


class OpenRig(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.env = env.Environment()
        self.rigs = []

        self.setupUI()
        self.updateUI()

    def setupUI(self):
        self.setWindowTitle("Open Rig")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowFullscreenButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowShadeButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
        self.setWindowFlags(QtCore.Qt.WindowTransparentForInput)
        self.setWindowFlags(QtCore.Qt.WindowOverridesSystemGestures)
        self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus)

        self.resize(300, 300)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.radioButtonLayout = QtWidgets.QHBoxLayout()

        self.characterRadioButton = QtWidgets.QRadioButton("Character")
        self.characterRadioButton.setChecked(True)
        self.characterRadioButton.toggled.connect(self.updateUI)
        self.radioButtonLayout.addWidget(self.characterRadioButton)

        self.propRadioButton = QtWidgets.QRadioButton("Prop")
        self.propRadioButton.toggled.connect(self.updateUI)
        self.radioButtonLayout.addWidget(self.propRadioButton)

        self.mainLayout.addLayout(self.radioButtonLayout)

        self.listWidget = QtWidgets.QListWidget()
        self.mainLayout.addWidget(self.listWidget)
        self.listWidget.addItems(self.rigs)
        self.listWidget.itemClicked.connect(self.updateButtonText)

        self.openRigButton = QtWidgets.QPushButton("Open Rig")
        self.openRigButton.clicked.connect(self.openRig)
        self.openRigButton.setDisabled(True)
        self.mainLayout.addWidget(self.openRigButton)

    def updateUI(self):
        self.getRigs()
        self.listWidget.clear()
        self.listWidget.addItems(self.rigs)

        self.updateButtonText()

    def getRigs(self):
        rigType = self.getRigType()
        if rigType == "character":
            self.rigs = os.listdir(self.env.get_rig_dir())
            if "props" in self.rigs:
                self.rigs.remove("props")
        elif rigType == "prop":
            self.rigs = os.listdir(self.env.get_rig_prop_dir())

    def getRigType(self):
        if self.characterRadioButton.isChecked():
            return "character"
        elif self.propRadioButton.isChecked():
            return "prop"

    def updateButtonText(self):
        if self.listWidget.currentItem():
            self.openRigButton.setDisabled(False)
            self.openRigButton.setText("Open Rig: " + self.listWidget.currentItem().text())
        else:
            self.openRigButton.setDisabled(True)
            self.openRigButton.setText("Open Rig")

    def openRig(self):
        if not self.listWidget.currentItem():
            return

        rigType = self.getRigType()
        if rigType == "character":
            rigFolder = os.path.join(self.env.get_rig_dir(), self.listWidget.currentItem().text())
        elif rigType == "prop":
            rigFolder = os.path.join(self.env.get_rig_prop_dir(), self.listWidget.currentItem().text())

        if not os.path.exists(rigFolder):
            mc.error("Rig folder does not exist: " + rigFolder)
            return

        # Look for the rig file
        rigFiles = os.listdir(rigFolder)
        rigFile = None
        for file in rigFiles:
            if file.endswith(".mb") or file.endswith(".ma"):
                rigFile = file
                break

        if not rigFile:
            mc.error("No rig file found in: " + rigFolder)
            return

        mc.file(os.path.join(rigFolder, rigFile), open=True, force=True)


class mayaRun:
    def run(self):
        rigUI = OpenRig()
        rigUI.exec_()
