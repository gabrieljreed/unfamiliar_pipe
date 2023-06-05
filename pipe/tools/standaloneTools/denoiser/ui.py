"""
Standalone denoiser tool. This tool is used to denoise renders from Houdini with idenoiser.

idenoise -d oidn -n nn -a albedo --aovs Ci a Nn motionBack z albedo beauty
directDiffuse directSpecular indirectDiffuse indirectSpecular subsurface
directSpecularGlassLobe indirectSpecularGlassLobe subsurfaceLobe
transmissiveGlassLobe shadow __depth  --options '{"blendfactor":0.75}'
IN_FILE.exr
OUT_FILE.exr
"""

from PySide2 import QtWidgets, QtCore, QtGui

import sys
import os
import shutil
import subprocess
import threading
import json

sys.path.append(r"/groups/unfamiliar/anim_pipeline")
sys.path.append(r"/groups/unfamiliar/anim_pipeline/pipe/vendor")

try:
    from tqdm import tqdm
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm


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

        self.defaultBlendFactor = 0.85

        # Load the json file
        jsonFile = json.load(open(jsonSettingsFilePath, "r"))
        self.aovs = ""
        for aov in jsonFile["AOVs"]:
            if aov == "u" or aov == "v":
                continue

            self.aovs += aov + " "

        self.setupUI()

    def setupUI(self) -> None:
        """Set up the UI."""
        self.setWindowTitle("Denoiser")
        self.setWindowIcon(QtGui.QIcon(':/icons/unwelleth.png'))

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)

        self.shotTab = QtWidgets.QWidget()
        self.frameTab = QtWidgets.QWidget()

        self.tabWidget.addTab(self.shotTab, "Denoise shots")
        self.tabWidget.addTab(self.frameTab, "Denoise frames")

        self.setupShotTab()
        self.setupFrameTab()

    def setupShotTab(self) -> None:
        """Set up the shot tab UI."""
        self.shotTabLayout = QtWidgets.QVBoxLayout(self.shotTab)

        self.searchBar = QtWidgets.QLineEdit()
        self.searchBar.setPlaceholderText("Search")
        self.searchBar.textChanged.connect(self.search)
        self.shotTabLayout.addWidget(self.searchBar)

        # LISTS
        self.listLayout = QtWidgets.QHBoxLayout()
        self.shotTabLayout.addLayout(self.listLayout)

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
        # self.shotListWidget.addItems(self.shots)
        self.shotLayout.addWidget(self.shotListWidget)

        self.sequenceListWidget.itemClicked.connect(self.updateUI)

        # SHOT DIRECTORIES
        def fillShotDirList():
            if self.shotListWidget.currentItem() is None:
                return

            self.shotDirList.clear()
            itemsToAdd = os.listdir(
                os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(), "render"))
            for item in itemsToAdd:
                if os.path.isfile(os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(), "render", item)):
                    # Remove it from itemsToAdd
                    itemsToAdd.remove(item)

            currentShot = self.shotListWidget.currentItem().text().lower()
            currentShotNoUnderscores = currentShot.replace("_", "").lower()

            for item in itemsToAdd:
                if not os.path.isdir(os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(), "render", item)):
                    continue
                if len(os.listdir(os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(), "render", item))) == 0:
                    continue

                # Add each item along with a checkbox
                listWidgetItem = QtWidgets.QListWidgetItem(item)
                listWidgetItem.setFlags(listWidgetItem.flags() | QtCore.Qt.ItemIsUserCheckable)

                formattedItem = item.lower()
                if "test" in formattedItem or formattedItem.startswith(currentShot) or formattedItem.startswith(currentShotNoUnderscores):
                    listWidgetItem.setCheckState(QtCore.Qt.Unchecked)
                else:
                    listWidgetItem.setCheckState(QtCore.Qt.Checked)
                self.shotDirList.addItem(listWidgetItem)

        self.shotListWidget.itemClicked.connect(fillShotDirList)

        self.shotDirList = QtWidgets.QListWidget()
        self.shotDirList.setAlternatingRowColors(True)
        self.shotTabLayout.addWidget(self.shotDirList)

        # BLEND FACTOR
        self.blendFactorLayout = QtWidgets.QHBoxLayout()
        self.shotTabLayout.addLayout(self.blendFactorLayout)

        self.blendFactorLabel = QtWidgets.QLabel("Blend Factor")
        self.blendFactorLayout.addWidget(self.blendFactorLabel)

        self.blendFactorLineEdit = QtWidgets.QLineEdit()
        self.blendFactorLineEdit.setText(str(self.defaultBlendFactor))
        self.blendFactorLayout.addWidget(self.blendFactorLineEdit)

        # RENDER TYPE
        self.renderTypeLayout = QtWidgets.QHBoxLayout()
        self.shotTabLayout.addLayout(self.renderTypeLayout)

        self.renderTypeLabel = QtWidgets.QLabel("Render Type")
        self.renderTypeLayout.addWidget(self.renderTypeLabel)

        self.renderTypeComboBox = QtWidgets.QComboBox()
        self.renderTypeComboBox.addItems(["Re-Denoise", "New Render"])
        self.renderTypeLayout.addWidget(self.renderTypeComboBox)

        self.renderTypeInfoButton = QtWidgets.QPushButton("i")
        self.renderTypeInfoButton.setFixedWidth(20)
        self.renderTypeInfoButton.clicked.connect(self.renderTypeInfo)
        self.renderTypeLayout.addWidget(self.renderTypeInfoButton)

        # BUTTONS
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.shotTabLayout.addLayout(self.buttonLayout)

        self.exportButton = QtWidgets.QPushButton("OK")
        self.exportButton.clicked.connect(self.denoise)
        self.buttonLayout.addWidget(self.exportButton)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.buttonLayout.addWidget(self.cancelButton)

        self.cancelButton.clicked.connect(self.close)

    def renderTypeInfo(self):
        """Show a message box with information about the render types."""
        QtWidgets.QMessageBox.information(self, "Render Types", "Re-Denoise: Run a new denoise pass on the same rendered images.\n\nNew Render: A new render is ready to be denoised. (WARNING: This deletes the 'undenoised' folder!).")

    def setupFrameTab(self) -> None:
        """Set up the frame tab UI."""
        self.frameTabLayout = QtWidgets.QVBoxLayout(self.frameTab)

        self.renderFolder = "Render Folder"

        def browseFolder():
            self.renderFolder = QtWidgets.QFileDialog.getExistingDirectory()
            self.updateFrameWidget()

        self.browseFolderButton = QtWidgets.QPushButton("Browse")
        self.browseFolderButton.clicked.connect(browseFolder)
        self.frameTabLayout.addWidget(self.browseFolderButton)

        self.frameWidget = QtWidgets.QListWidget()
        self.frameTabLayout.addWidget(self.frameWidget)
        self.frameWidget.setDisabled(True)

        self.frameWidgetLayout = QtWidgets.QVBoxLayout(self.frameWidget)

        self.renderFolderLabel = QtWidgets.QLabel(self.renderFolder)
        self.frameWidgetLayout.addWidget(self.renderFolderLabel)

        self.frameList = QtWidgets.QListWidget()
        self.frameList.setAlternatingRowColors(True)
        self.frameWidgetLayout.addWidget(self.frameList)

        self.aovList = QtWidgets.QListWidget()
        self.aovList.setAlternatingRowColors(True)
        self.frameWidgetLayout.addWidget(self.aovList)

        for aov in self.aovs.split(" "):
            if aov == "" or aov == " ":
                continue
            listWidgetItem = QtWidgets.QListWidgetItem(aov)
            listWidgetItem.setFlags(listWidgetItem.flags() | QtCore.Qt.ItemIsUserCheckable)
            listWidgetItem.setCheckState(QtCore.Qt.Checked)
            self.aovList.addItem(listWidgetItem)

        # BLEND FACTOR
        self.frameBlendFactorLayout = QtWidgets.QHBoxLayout()
        self.frameWidgetLayout.addLayout(self.frameBlendFactorLayout)

        self.blendFactorLabel = QtWidgets.QLabel("Blend Factor")
        self.frameBlendFactorLayout.addWidget(self.blendFactorLabel)

        self.blendFactorLineEdit = QtWidgets.QLineEdit()
        self.blendFactorLineEdit.setText(str(self.defaultBlendFactor))
        self.frameBlendFactorLayout.addWidget(self.blendFactorLineEdit)

        self.denoiseFrameButton = QtWidgets.QPushButton("Denoise Frame(s)")
        self.denoiseFrameButton.clicked.connect(self.denoiseFrame)
        self.frameWidgetLayout.addWidget(self.denoiseFrameButton)

    def updateFrameWidget(self):
        """Update the frame widget when the user browses for a folder."""
        self.frameWidget.setDisabled(False)

        self.renderFolderLabel.setText(os.path.basename(self.renderFolder))
        self.renderFolderLabel.setToolTip(self.renderFolder)

        self.frameList.clear()
        frames = os.listdir(self.renderFolder)
        frames.sort()

        for frame in frames:
            if os.path.isdir(os.path.join(self.renderFolder, frame)):
                continue

            listWidgetItem = QtWidgets.QListWidgetItem(frame)
            listWidgetItem.setFlags(listWidgetItem.flags() | QtCore.Qt.ItemIsUserCheckable)
            listWidgetItem.setCheckState(QtCore.Qt.Unchecked)
            self.frameList.addItem(listWidgetItem)

    def updateUI(self):
        """Update the UI when a sequence is clicked on."""
        self.shotListWidget.clear()
        self.shotListWidget.addItems(self.getShots())

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

        if self.renderTypeComboBox.currentText() == "New Render":
            foldersToDelete = []
            totalFoldersToDelete = 0
            totalFilesToDelete = 0
            for item in checkedItems:
                undenoisedFolderPath = os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(),
                                                    "render", item, "undenoised")
                if not os.path.isdir(undenoisedFolderPath):
                    continue
                foldersToDelete.append(undenoisedFolderPath)
                totalFoldersToDelete += 1
                totalFilesToDelete += len(os.listdir(undenoisedFolderPath))

            if totalFoldersToDelete > 0:
                reply = QtWidgets.QMessageBox.question(
                    self,
                    "Delete Undenoised Folders?",
                    "Are you sure you want to delete {} undenoised folders and {} files?".format(
                        totalFoldersToDelete, totalFilesToDelete
                    ),
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No
                )

                if reply == QtWidgets.QMessageBox.No:
                    return

                for folder in foldersToDelete:
                    shutil.rmtree(folder)
                    print(f"Deleted {folder}")

        for item in checkedItems:
            itemPath = os.path.join(self.env.get_shot_dir(), self.shotListWidget.currentItem().text(), "render", item)

            def denoiseFolder(folderPath):
                images = os.listdir(folderPath)
                images.sort()

                if not os.path.exists(os.path.join(folderPath, "undenoised")):
                    os.makedirs(os.path.join(folderPath, "undenoised"))

                    for f in images:
                        if not os.path.isfile(os.path.join(folderPath, f)):
                            continue

                        shutil.move(os.path.join(folderPath, f), os.path.join(folderPath, "undenoised", f))

                images = os.listdir(os.path.join(folderPath, "undenoised"))

                errors = []

                # for i, img in enumerate(images):
                for img in tqdm(images, desc=os.path.basename(folderPath)):
                    blendFactorCommand = '\'{"blendfactor":' + str(blendFactor) + '}\''

                    inPath = os.path.join(folderPath, "undenoised", img)
                    outPath = os.path.abspath(os.path.join(folderPath, img))
                    # command = f"idenoise -d oidn -n nn -a albedo --aovs {self.aovs} --options {blendFactorCommand} {inPath} {outPath}"
                    command = f"idenoise {inPath} {outPath} -d oidn -n nn -a albedo --options {blendFactorCommand} --aovs C a Cf Color Ci Nn motionBack z albedo beauty directDiffuse directSpecular indirectDiffuse indirectSpecular subsurface directSpecularGlassLobe indirectSpecularGlassLobe subsurfaceLobe transmissiveGlassLobe shadow __depth"

                    result = subprocess.run(
                        command, cwd=folderPath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    stdout = result.stdout
                    if stdout is not None:
                        stdout = stdout.decode("utf-8")
                        if len(stdout) > 0:
                            print(stdout)
                            errors.append(f"{img}: {stdout}")

                permissions.set_permissions(folderPath)
                print(f"Finished denoising {os.path.basename(folderPath)}. ({len(images)} images denoised)")
                if len(errors) > 0:
                    print(f"{len(errors)} Errors:")
                    for error in errors:
                        print(error)

            # Start a thread for each folder
            thread = threading.Thread(target=denoiseFolder, args=(itemPath,))
            thread.start()

    def denoiseFrame(self):
        """Denoise individual frame(s)."""
        framesToDenoise = []

        for i in range(self.frameList.count()):
            item = self.frameList.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                framePath = os.path.join(self.renderFolder, item.text())
                framesToDenoise.append(framePath)

        aovs = []
        for i in range(self.aovList.count()):
            item = self.aovList.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                aovs.append(item.text())

        aovs = " ".join(aovs)

        blendFactor = self.blendFactorLineEdit.text()
        blendFactorCommand = '\'{"blendfactor":' + str(blendFactor) + '}\''
        for frame in framesToDenoise:
            print(f"Denoising {os.path.basename(frame)}")
            inPath = frame
            outPath = os.path.abspath(os.path.join(self.renderFolder, os.pardir, os.path.basename(frame)))
            command = f"idenoise {inPath} {outPath} -d oidn -n nn -a albedo --options {blendFactorCommand} --aovs {aovs}"
            result = subprocess.run(command, cwd=os.path.dirname(frame), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            permissions.set_permissions(outPath)

            stdout = result.stdout
            if stdout is not None:
                stdout = stdout.decode("utf-8")
                if len(stdout) > 0:
                    print(stdout)
                else:
                    print(f"Denoising successful!\nDenoised frame located at {outPath}")


if __name__ == '__main__':
    # import time
    # for i in tqdm(range(5)):
    #     time.sleep(1)
    app = QtWidgets.QApplication(sys.argv)
    denoiser = DenoiserWidget()
    denoiser.show()
    sys.exit(app.exec_())
