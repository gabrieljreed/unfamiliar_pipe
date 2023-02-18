"""The UI that will be launched to prompt the user"""
from PySide2 import QtWidgets, QtCore, QtGui

import sys
import os
import subprocess


class ImageToMovWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.inFilePath = "None Selected"
        self.outFilePath = "None Selected"

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Image Sequence to .mov Converter")
        self.setWindowIcon(QtGui.QIcon(':/icons/videoConverter.png'))
        self.resize(400, 300)
        self.setMinimumSize(400, 300)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        # self.mainLayout.setContentsMargins(0, 0, 0, 0)
        # self.mainLayout.setSpacing(0)

        self.mainLayout.addWidget(QtWidgets.QLabel("Directory of Image Sequence"))

        self.inFilePathLabel = QtWidgets.QLabel(self.inFilePath)
        self.inFilePathLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.inFilePathLabel)

        self.browseInButton = QtWidgets.QPushButton("Browse")
        self.browseInButton.clicked.connect(self.browseIn)
        self.browseInButton.setFixedWidth(75)
        self.mainLayout.addWidget(self.browseInButton)

        spacerWidget = QtWidgets.QWidget()
        spacerWidget.setFixedHeight(50)
        self.mainLayout.addWidget(spacerWidget)

        self.mainLayout.addWidget(QtWidgets.QLabel("Export Directory"))

        self.outFilePathLabel = QtWidgets.QLabel(self.outFilePath)
        self.outFilePathLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.outFilePathLabel)

        self.browseOutButton = QtWidgets.QPushButton("Browse")
        self.browseOutButton.clicked.connect(self.browseOut)
        self.browseOutButton.setFixedWidth(75)
        self.mainLayout.addWidget(self.browseOutButton)

        spacerWidget = QtWidgets.QWidget()
        spacerWidget.setFixedHeight(50)
        self.mainLayout.addWidget(spacerWidget)

        self.convertButton = QtWidgets.QPushButton("Convert")
        self.convertButton.clicked.connect(self.convert)
        self.convertButton.setFixedWidth(75)
        self.mainLayout.addWidget(self.convertButton)

    def updateUI(self):
        self.inFilePathLabel.setText(self.inFilePath)
        self.outFilePathLabel.setText(self.outFilePath)

    def browseIn(self):
        """Launches a file picker for inFilePath"""
        self.inFilePath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory of Image Sequence")
        if self.inFilePath is not None and self.inFilePath != "":
            self.updateUI()

    def browseOut(self):
        """Launches a file picker for outFilePath"""
        # TODO: Set default start location
        self.outFilePath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if self.outFilePath is not None and self.outFilePath != "":
            self.updateUI()

    def convert(self):
        """Does the conversion"""
        if self.inFilePath == "None Selected" or self.outFilePath == "None Selected":
            return

        command = """
export MEDIA_PROJECT_DIR=/groups/unfamiliar/anim_pipeline
export MEDIA_PIPE_DIR=$MEDIA_PROJECT_DIR/pipe
#Environment variable for location of python scripts
export PYTHONPATH=${MEDIA_PROJECT_DIR}:${MEDIA_PIPE_DIR}:${MEDIA_PROJECT_DIR}/lib/
unset OCIO

export NUKE_PATH=${MEDIA_PROJECT_DIR}/pipe:${MEDIA_PROJECT_DIR}/pipe/tools/nukeTools:${MEDIA_PROJECT_DIR}/lib/NukeSurvivalToolkit

        """

        pythonFile = os.path.normpath(os.path.join(os.path.dirname(__file__), "convert.py"))

        inFileType = os.listdir(self.inFilePath)[0].split(".")[-1]
        totalLen = len(os.listdir(self.inFilePath))
        baseName = os.path.basename(self.inFilePath)

        lastLine = f"/opt/Nuke13.2v2/Nuke13.2 -t {pythonFile} {self.inFilePath}/{baseName}.####.{inFileType} {self.outFilePath}/{baseName}.mov 1,{totalLen}"
        command += "\n" + lastLine

        print(command)

        self.convertButton.setText("Converting...")
        self.convertButton.setDisabled(True)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print(line)
        retval = p.wait()
        self.convertButton.setText("Convert")
        self.convertButton.setDisabled(False)

        print("Done")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open(':/stylesheets/videoConverter.qss').read())
    videoConverter = ImageToMovWidget()
    videoConverter.show()
    sys.exit(app.exec_())
