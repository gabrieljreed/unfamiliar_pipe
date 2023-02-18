from PySide2 import QtWidgets, QtCore, QtGui

import nuke
import os

import pipe.tools.pythonTools.stringUtilities as stringUtilities
import pipe.pipeHandlers.environment as env

import pipe.pipeHandlers.quick_dialogs as qd


def getCurrentShot() -> str:
    """Returns the current shot if it can be detected, otherwise launches a dialog to prompt the user to pick the shot
    they're working on"""
    try:
        currentNukeFile = os.path.basename(nuke.scriptName())
        if currentNukeFile.endswith(".nk"):
            currentNukeFile = stringUtilities.stripSuffix(currentNukeFile, ".nk")
        if currentNukeFile.endswith("_main"):
            currentNukeFile = stringUtilities.stripSuffix(currentNukeFile, "_main")

    except Exception:
        print("File is not saved, pick a shot to export to")
        dialog = qd.ShotSelectDialog()
        if dialog.exec_():
            return dialog.selectedShot()
        # TODO: Launch a dialog to prompt the user to pick a shot
        return "None"

    return currentNukeFile


def sequenceShotDialog() -> str:
    """Launches a dialog that prompts the user to select a sequence, then a shot. Returns the shot name as a string"""
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Select a sequence and shot")
    dialog.setFixedSize(325, 200)

    mainWidget = QtWidgets.QWidget()
    mainLayout = QtWidgets.QVBoxLayout(mainWidget)
    mainWidget.setLayout(mainLayout)
    dialog.setCentralWidget(mainWidget)

    listHolder = QtWidgets.QHBoxLayout()
    mainLayout.addLayout(listHolder)

    sequenceListWidget = QtWidgets.QListWidget()
    sequenceListWidget.setAlternatingRowColors(True)
    sequenceListWidget.setFixedWidth(150)
    listHolder.addWidget(sequenceListWidget)

    shotListWidget = QtWidgets.QListWidget()
    shotListWidget.setAlternatingRowColors(True)
    shotListWidget.setFixedWidth(150)
    listHolder.addWidget(shotListWidget)


def exrExport():
    """Creates a write node preconfigured for EXR exporting"""
    currentShot = getCurrentShot()
    file = os.path.join(env.Environment().project_dir, "production", "edit", "shots", "exr_sequences", currentShot,
                        currentShot + ".###.exr")
    n = nuke.nodes.Write(file=file, file_type="exr", write_ACES_compliant_EXR=True, create_directories=True,
                         name="EXR Export")

    return n


def movExport():
    """Creates a write node preconfigured for MOV exporting"""
    currentShot = getCurrentShot()
    file = os.path.join(env.Environment().project_dir, "production", "edit", "shots", "05_temp_mp4", currentShot,
                        currentShot + ".mov")
    n = nuke.nodes.Write(file=file, file_type="mov", mov_prores_codec_profile="ProRes 4:4:4:4 XQ 12-bit",
                         colorspace="color_picking", create_directories=True, name="MOV Export")

    return n
