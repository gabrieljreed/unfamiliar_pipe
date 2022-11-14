import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import os
import sys


class VideoConverter(QtWidgets.QWidget):
    def __init__(self):
        super(VideoConverter, self).__init__()
        self.setWindowTitle('Video Converter')
        self.setWindowIcon(QtGui.QIcon(':/icons/videoConverter.png'))
        self.resize(400, 300)
        self.setMinimumSize(400, 300)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.topWidget = QtWidgets.QWidget(self)
        self.topWidget.setObjectName('topWidget')
        self.topLayout = QtWidgets.QVBoxLayout(self.topWidget)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setSpacing(0)

        self.videoWidget = QtWidgets.QWidget(self.topWidget)
        self.videoWidget.setObjectName('videoWidget')
        self.videoLayout = QtWidgets.QHBoxLayout(self.videoWidget)
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout.setSpacing(0)
        self.topLayout.addWidget(self.videoWidget)

        self.videoLabel = QtWidgets.QLabel(self.topWidget)
        self.videoLabel.setObjectName('videoLabel')
        self.videoLabel.setText('Video:')
        self.videoLayout.addWidget(self.videoLabel)

        self.videoLineEdit = QtWidgets.QLineEdit(self.topWidget)
        self.videoLineEdit.setObjectName('videoLineEdit')
        self.videoLineEdit.setReadOnly(True)
        self.videoLayout.addWidget(self.videoLineEdit)

        self.videoButton = QtWidgets.QPushButton(self.topWidget)
        self.videoButton.setObjectName('videoButton')
        self.videoButton.setText('...')
        self.videoLayout.addWidget(self.videoButton)

        self.mainLayout.addWidget(self.topWidget)

        self.bottomWidget = QtWidgets.QWidget(self)
        self.bottomWidget.setObjectName('bottomWidget')
        self.bottomLayout = QtWidgets.QHBoxLayout(self.bottomWidget)
        self.bottomLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomLayout.setSpacing(0)

        self.convertButton = QtWidgets.QPushButton(self.bottomWidget)
        self.convertButton.setObjectName('convertButton')
        self.convertButton.setText('Convert')
        self.bottomLayout.addWidget(self.convertButton)

        self.mainLayout.addWidget(self.bottomWidget)

        self.videoButton.clicked.connect(self.videoButtonClicked)
        self.convertButton.clicked.connect(self.convertButtonClicked)

        # Specify bitrate 
        self.bitrate = 5000
        # Bitrate UI 
        self.bitrateWidget = QtWidgets.QWidget(self)
        self.bitrateWidget.setObjectName('bitrateWidget')
        self.bitrateLayout = QtWidgets.QHBoxLayout(self.bitrateWidget)
        self.bitrateLayout.setContentsMargins(0, 0, 0, 0)
        self.bitrateLayout.setSpacing(0)
        self.topLayout.addWidget(self.bitrateWidget)

        self.bitrateLabel = QtWidgets.QLabel(self.topWidget)
        self.bitrateLabel.setObjectName('bitrateLabel')
        self.bitrateLabel.setText('Bitrate:')
        self.bitrateLayout.addWidget(self.bitrateLabel)

        self.bitrateLineEdit = QtWidgets.QLineEdit(self.topWidget)
        self.bitrateLineEdit.setObjectName('bitrateLineEdit')
        self.bitrateLineEdit.setText(str(self.bitrate))
        self.bitrateLayout.addWidget(self.bitrateLineEdit)

        # Specify output file type 
        self.fileType = 'mp4'
        # Filetype UI
        self.fileTypeWidget = QtWidgets.QWidget(self.topWidget)
        self.fileTypeWidget.setObjectName('fileTypeWidget')
        self.fileTypeLayout = QtWidgets.QHBoxLayout(self.fileTypeWidget)
        self.fileTypeLayout.setContentsMargins(0, 0, 0, 0)
        self.fileTypeLayout.setSpacing(0)
        self.topLayout.addWidget(self.fileTypeWidget)

        self.filetypeLabel = QtWidgets.QLabel(self.topWidget)
        self.filetypeLabel.setObjectName('filetypeLabel')
        self.filetypeLabel.setText('Filetype:')
        self.fileTypeLayout.addWidget(self.filetypeLabel)

        self.filetypeLineEdit = QtWidgets.QLineEdit(self.topWidget)
        self.filetypeLineEdit.setObjectName('filetypeLineEdit')
        self.filetypeLineEdit.setText(self.fileType)
        self.fileTypeLayout.addWidget(self.filetypeLineEdit)

    def videoButtonClicked(self):
        videoPath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Video', '', 'Video Files (*.mp4 *.avi *.mov)')[0]
        if videoPath:
            self.videoLineEdit.setText(videoPath)

    def convertButtonClicked(self):
        videoPath = self.videoLineEdit.text()
        self.bitrate = self.bitrateLineEdit.text()
        self.fileType = self.filetypeLineEdit.text()
        if videoPath:
            videoName = os.path.basename(videoPath)
            videoName = os.path.splitext(videoName)[0]
            outputPath = os.path.join(os.path.dirname(videoPath), videoName)
            command = 'ffmpeg -i {} -b:v {}k {}.{}'.format(videoPath, self.bitrate, outputPath, self.fileType)
            # Run command in terminal
            os.system(command)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open(':/stylesheets/videoConverter.qss').read())
    videoConverter = VideoConverter()
    videoConverter.show()
    sys.exit(app.exec_())
