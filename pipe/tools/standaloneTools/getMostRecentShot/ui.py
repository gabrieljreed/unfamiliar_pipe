"""This is the UI for the getMostRecentShot tool."""

import pipe.pipeHandlers.quick_dialogs as qd
import pipe.tools.nukeTools.filmBuilder.filmBuilder as fb

from PySide2 import QtWidgets
import os
import sys
import json


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    shotDialog = qd.ShotSelectDialog()

    shotDialog.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    shotDialog.setMinimumSize(400, 400)

    if not shotDialog.exec_():
        sys.exit()

    shot = shotDialog.selectedShot()
    mostRecentVersion = fb.getMostRecentShotVersion(shotName=shot)
    fullPath = os.path.join(f"/groups/unfamiliar/anim_pipeline/production/edit/shots", mostRecentVersion, shot)

    # Message box to show the most recent version and open the folder
    msgBox = QtWidgets.QMessageBox()
    msgBox.setWindowTitle("Most Recent Version")
    msgBox.setText(f"The most recent version of {shot} is {mostRecentVersion}")
    msgBox.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
    openFolderButton = QtWidgets.QPushButton("Open Folder")
    openFolderButton.clicked.connect(lambda: os.system('xdg-open "%s"' % fullPath))
    if os.path.exists(fullPath):
        msgBox.addButton(openFolderButton, QtWidgets.QMessageBox.AcceptRole)
    msgBox.exec_()

    sys.exit()
