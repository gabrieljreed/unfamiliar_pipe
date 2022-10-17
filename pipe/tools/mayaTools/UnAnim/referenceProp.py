import os

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import maya.cmds as mc

PROP_PATH = os.path.join(os.environ["MEDIA_PROJECT_DIR"], "production", "rigs", "props")


class ReferenceProp(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.props = os.listdir(PROP_PATH)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Reference prop for Animation")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setMinimumSize(300, 300)
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.environ["MEDIA_PROJECT_DIR"], "icons", "frog.png")))

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.mainLayout.setSpacing(2)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.centralWidget.setLayout(self.mainLayout)

        self.instructionLabel = QtWidgets.QLabel("Select a prop to reference")
        self.mainLayout.addWidget(self.instructionLabel)

        self.propList = QtWidgets.QListWidget()
        self.propList.setAlternatingRowColors(True)
        self.propList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.propList.addItems(self.props)
        self.mainLayout.addWidget(self.propList)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(2)
        self.buttonLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.buttonLayout)

        self.referenceButton = QtWidgets.QPushButton("Reference")
        self.referenceButton.clicked.connect(self.reference)
        self.buttonLayout.addWidget(self.referenceButton)

        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.buttonLayout.addWidget(self.closeButton)

    def reference(self):
        for item in self.propList.selectedItems():
            prop = item.text()
            propPath = os.path.join(PROP_PATH, prop, prop + ".mb")
            mc.file(propPath, reference=True, namespace=prop)


class mayaRun:
    def run(self):
        self.ui = ReferenceProp()
        self.ui.show()
