from PySide2 import QtWidgets, QtCore, QtGui

import sys
import os
import subprocess
import threading
import json

sys.path.append(r"/groups/unfamiliar/anim_pipeline")

import pipe.pipeHandlers.environment as env
import pipe.pipeHandlers.permissions as permissions


jsonSettingsFilePath = "/groups/unfamiliar/anim_pipeline/pipe/tools/houdiniTools/render/render_settings.json"


class DenoiserWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.env = env.Environment()
        self.baseDir = os.path.abspath(os.path.join(self.env.project_dir, os.pardir, "Editing", "Animation"))

        self.sequences = self.getSequences()
        self.shots = []

        self.defaultBlendFactor = 0.75

        # Load the json file
        jsonFile = json.load(open(jsonSettingsFilePath, "r"))
        self.aovs = ""
        for aov in jsonFile["AOVs"]:
            if aov == "u" or aov == "v":
                continue

            self.aovs += aov + " "

        self.setupUI()

    def setupUI(self) -> None:
        self.setWindowTitle("Lock shots for render")
        self.setWindowIcon(QtGui.QIcon(':/icons/unwelleth.png'))

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.searchBar = QtWidgets.QLineEdit()
        self.searchBar.setPlaceholderText("Search")
        self.searchBar.textChanged.connect(self.search)
        self.mainLayout.addWidget(self.searchBar)

        # LISTS
        self.listLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.listLayout)

        self.sequenceLayout = QtWidgets.QVBoxLayout()
        self.listLayout.addLayout(self.sequenceLayout)

        self.sequenceLabel = QtWidgets.QLabel("Sequences")
        self.sequenceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sequenceLayout.addWidget(self.sequenceLabel)

        self.sequenceListWidget = QtWidgets.QListWidget()
        self.sequenceListWidget.setFixedWidth(150)
        self.sequenceListWidget.addItems(self.sequences)
        self.sequenceLayout.addWidget(self.sequenceListWidget)

        self.shotLayout = QtWidgets.QVBoxLayout()
        self.listLayout.addLayout(self.shotLayout)

        self.shotLabel = QtWidgets.QLabel("Shots")
        self.shotLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.shotLayout.addWidget(self.shotLabel)

        self.shotListWidget = QtWidgets.QListWidget()
        self.shotListWidget.setFixedWidth(150)
        for shot in self.shots:
            listWidgetItem = QtWidgets.QListWidgetItem(shot)
            listWidgetItem.setFlags(listWidgetItem.flags() | QtCore.Qt.ItemIsUserCheckable)
            listWidgetItem.setCheckState(QtCore.Qt.Unchecked)
            self.shotListWidget.addItem(listWidgetItem)

        self.shotLayout.addWidget(self.shotListWidget)

        self.sequenceListWidget.itemClicked.connect(self.updateUI)

        self.shotDirList = QtWidgets.QListWidget()
        self.shotDirList.setAlternatingRowColors(True)
        self.mainLayout.addWidget(self.shotDirList)

        # BUTTONS
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.exportButton = QtWidgets.QPushButton("OK")
        self.exportButton.clicked.connect(self.denoise)
        self.buttonLayout.addWidget(self.exportButton)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.buttonLayout.addWidget(self.cancelButton)

        self.cancelButton.clicked.connect(self.close)

    def updateUI(self):
        self.shotListWidget.clear()
        self.shots = self.getShots()

        for shot in self.shots:
            listWidgetItem = QtWidgets.QListWidgetItem(shot)
            listWidgetItem.setFlags(listWidgetItem.flags() | QtCore.Qt.ItemIsUserCheckable)
            listWidgetItem.setCheckState(QtCore.Qt.Unchecked)
            # connect checking the item to the function that will update the UI
            self.shotListWidget.addItem(listWidgetItem)

        self.shotListWidget.itemClicked.connect(self.updateShotDirList)

    def updateShotDirList(self):
        print("Here")

    def search(self):
        search = self.searchBar.text()
        self.sequenceListWidget.clear()
        self.shotListWidget.clear()
        if search == "":
            self.sequenceListWidget.addItems(self.sequences)
            self.shotListWidget.addItems(self.shots)
        else:
            self.sequenceListWidget.addItems([s for s in self.sequences if search in s])
            self.shotListWidget.addItems([s for s in self.getAllShots() if search in s])

    def getSequences(self):
        """Returns an alphabetically sorted list of sequences in the project.
        @return: list of sequences"""

        sequences = [d for d in os.listdir(self.baseDir) if d.startswith(("SEQ"))]
        sequences.sort()
        return sequences

    def getShots(self):
        """Returns a list of shots in the current sequence. Returns an empty list if no sequence is selected.
        @return: list of shots"""

        if self.sequenceListWidget.currentItem() is None:
            return []

        currentSequence = self.sequenceListWidget.currentItem().text()[-1]
        # shots = os.listdir(os.path.join(self.baseDir, currentSequence))
        shots = os.listdir(self.env.get_shot_dir())
        shots = [shot for shot in shots if shot.startswith(currentSequence)]
        shots.sort()
        return shots

    def getAllShots(self):
        shots = os.listdir(self.env.get_shot_dir())
        shots.sort()
        return shots

    def denoise(self):
        # Get a list of all checked items in the shotDirList
        checkedItems = [self.shotDirList.item(i).text() for i in range(self.shotDirList.count()) if
                        self.shotDirList.item(i).checkState() == QtCore.Qt.Checked]

        blendFactor = self.blendFactorLineEdit.text()

        for item in checkedItems:
            itemPath = os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(), "render", item)

            def denoiseFolder(folderPath):
                images = os.listdir(folderPath)
                images.sort()

                if "denoised" in images:
                    images.remove("denoised")

                if os.path.exists(os.path.join(folderPath, "denoised")):
                    for f in os.listdir(os.path.join(folderPath, "denoised")):
                        os.remove(os.path.join(folderPath, "denoised", f))
                else:
                    os.makedirs(os.path.join(folderPath, "denoised"))

                for i, img in enumerate(images):
                    blendFactorCommand = '\'{"blendfactor":' + str(blendFactor) + '}\''

                    inPath = os.path.join(folderPath, img)
                    outPath = os.path.join(folderPath, "denoised", "denoised_" + img)
                    command = f"idenoise -d oidn -n nn -a albedo --aovs {self.aovs} --options {blendFactorCommand} {inPath} {outPath}"

                    subprocess.call(command, cwd=folderPath, shell=True)

                permissions.set_permissions(folderPath)
                print(f"Finished denoising {folderPath}. ({len(images)} images denoised)")

            # Start a thread for each folder
            thread = threading.Thread(target=denoiseFolder, args=(itemPath,))
            thread.start()
            print(f"Started thread for {itemPath}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open(':/stylesheets/videoConverter.qss').read())
    videoConverter = DenoiserWidget()
    videoConverter.show()
    sys.exit(app.exec_())
