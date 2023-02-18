import sys
sys.path.append('/groups/unfamiliar/anim_pipeline/')
import os
import json
from PySide2 import QtWidgets, QtCore, QtGui
import pipe.pipeHandlers.quick_dialogs as qd


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    shotDialog = qd.ShotSelectDialog()
    mayaRadioButton = QtWidgets.QRadioButton("Maya")
    houdiniRadioButton = QtWidgets.QRadioButton("Houdini")
    houdiniRadioButton.setChecked(True)
    radioButtonLayout = QtWidgets.QHBoxLayout()
    radioButtonLayout.addWidget(mayaRadioButton)
    radioButtonLayout.addWidget(houdiniRadioButton)
    shotDialog.mainLayout.addLayout(radioButtonLayout)

    # Make the shot dialog resizable
    shotDialog.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    shotDialog.setMinimumSize(400, 400)

    # wrapperWidget = QtWidgets.QWidget()
    # wrapperWidget.layout().addWidget(shotDialog)

    # wrapperWidget.show()

    if not shotDialog.exec_():
        sys.exit()

    if mayaRadioButton.isChecked():
        shotPath = os.path.join("/groups/unfamiliar/anim_pipeline/production/anim_shots", shotDialog.selectedShot())
    elif houdiniRadioButton.isChecked():
        shotPath = os.path.join("/groups/unfamiliar/anim_pipeline/production/shots", shotDialog.selectedShot())
    elementPath = os.path.join(shotPath, ".element")
    print(elementPath)
    if not os.path.exists(elementPath):
        print("No element file found")
        sys.exit()

    with open(elementPath, "r") as f:
        elementData = json.load(f)

    elementData["assigned_user"] = ""

    with open(elementPath, "w") as f:
        json.dump(elementData, f, indent=4)

    sys.exit(app.exec_())
