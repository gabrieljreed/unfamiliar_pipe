import os
from PySide2 import QtWidgets, QtCore, QtGui
import threading

import sys
sys.path.append(os.path.dirname(__file__))

import filmBuilder


class FilmBuilderUI(QtWidgets.QWidget):
    def __init__(self):
        super(FilmBuilderUI, self).__init__()
        self.buildUI()

    def buildUI(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(QtWidgets.QLabel("Sequences:"))
        self.radioButtons = []
        for sequence in filmBuilder.sequences:
            # Create a radio button for the sequence and add it to the layout
            sequenceButton = QtWidgets.QRadioButton(sequence)
            self.mainLayout.addWidget(sequenceButton)
            self.radioButtons.append(sequenceButton)

        self.mainLayout.addWidget(QtWidgets.QLabel("Entire film:"))

        filmButton = QtWidgets.QRadioButton("Build entire film")
        self.mainLayout.addWidget(filmButton)
        self.radioButtons.append(filmButton)

        self.buildButton = QtWidgets.QPushButton("Build")
        self.buildButton.clicked.connect(self.buildFilm)
        self.mainLayout.addWidget(self.buildButton)

    def buildFilm(self):
        # Get the currently selected radio button
        selected = None
        for button in self.radioButtons:
            if button.isChecked():
                selected = button.text()
                break

        if selected is None:
            print("Nothing selected")
            return

        if selected == "Build entire film":
            thread = threading.Thread(target=filmBuilder.buildFilm)
            thread.start()
        else:
            thread = threading.Thread(target=filmBuilder.buildSequence, args=(selected,))
            thread.start()

        # self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = FilmBuilderUI()
    window.setWindowTitle("Film Builder")
    window.setMinimumSize(400, 400)
    window.show()
    app.exec_()
