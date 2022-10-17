# Please dont ask me about this one I didn't care to learn PySide
# so this is copied directly from Stonk's Cenote pipe

from PySide2 import QtWidgets, QtCore, QtGui
import os  # , hou        we can't have import hou here because it makes it break on the maya side
from pipe.pipeHandlers.environment import Environment as env


def error(errMsg, details=None, title='Error'):
    '''Reports a critical error'''
    message(errMsg, details=details, title=title)


def warning(warnMsg, details=None, title='Warning'):
    '''Reports a non-critical warning'''
    message(warnMsg, details=details, title=title)


def message(msg=' ', details=None, title='Message'):
    '''Reports a message'''
    print(msg)

    msgBox = QtWidgets.QMessageBox()
    msgBox.setText(msgBox.tr(msg))
    if title == 'Warning':
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    elif title == 'Error':
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
    else:
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
    msgBox.setWindowTitle(title)
    msgBox.addButton(QtWidgets.QMessageBox.Ok)

    if details is not None:
        msgBox.setDetailedText(str(details))

    msgBox.exec_()


def info(infoMsg, title='Info'):
    '''Reports an informational message'''
    message(msg=infoMsg, title=title)


def light_error(errMsg, title='Warning'):
    '''Reports an error that can be resolved with a yes or no
    returns True if yes, otherwise False'''
    return yes_or_no(errMsg, title=title)


def yes_or_no(question, details=None, title='Question'):
    '''Asks a question that can be resolved with a yes or no
    returns True if yes, otherwise False'''
    msgBox = QtWidgets.QMessageBox()
    msgBox.setText(msgBox.tr(question))
    msgBox.setWindowTitle(title)
    if title == 'Question':
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
    else:
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    noButton = msgBox.addButton(QtWidgets.QMessageBox.No)
    yesButton = msgBox.addButton(QtWidgets.QMessageBox.Yes)

    if details is not None:
        msgBox.setDetailedText(details)

    msgBox.exec_()

    if msgBox.clickedButton() == yesButton:
        return True
    elif msgBox.clickedButton() == noButton:
        return False


def input(label, title='Input', text=None):
    '''
    Allows the user to respond with a text input
    If the okay button is pressed it returns the inputed text, otherwise None
    '''
    dialog = QtWidgets.QInputDialog()
    text = dialog.getText(None, title, label, text=text)

    if text[1]:
        return text[0]
    else:
        return None


def chooseFile(parent=None, caption=None, dir="/"):
    '''
    Allows the user to select a file location
    '''
    fileName = QtWidgets.QFileDialog.getSaveFileName(parent, caption, dir)
    return fileName


class HoudiniInput(QtWidgets.QDialog):
    '''
    submitted is a class variable that must be instantiated outside of __init__
    in order for the Signal to be created correctly.
    Have to use this instead of input in houdini to avoid black text on black bar
    '''
    submitted = QtCore.Signal(list)

    def __init__(self, parent=None, title="Enter info", info="", width=350, height=75):
        super(HoudiniInput, self).__init__(parent)

        self.info = info
        if parent:
            self.parent = parent
        self.setWindowTitle(title)
        self.setObjectName('HoudiniInput')
        self.resize(width, height)
        self.initializeVBox()
        self.setLayout(self.vbox)
        self.show()

    def initializeVBox(self):
        self.vbox = QtWidgets.QVBoxLayout()
        # QApplication.setActiveWindow()
        self.initializeInfoText()
        self.initializeTextBar()
        self.initializeSubmitButton()

    def initializeInfoText(self):
        info_text = QtWidgets.QLabel()
        info_text.setText(self.info)
        self.vbox.addWidget(info_text)

    def initializeTextBar(self):
        hbox = QtWidgets.QHBoxLayout()
        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setStyleSheet(
            "color: white; selection-color: black; selection-background-color: white;")
        self.text_input.textEdited.connect(self.textEdited)
        self.text_input.setFocus()
        hbox.addWidget(self.text_input)
        self.vbox.addLayout(hbox)

    def initializeSubmitButton(self):
        # Create the button widget
        self.button = QtWidgets.QPushButton("Confirm")
        self.button.setDefault(True)
        self.button.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.button.clicked.connect(self.submit)
        self.button.setEnabled(False)
        self.vbox.addWidget(self.button)

    def textEdited(self, newText):
        if len(newText) > 0:
            self.button.setEnabled(True)
            self.button.setDefault(True)
        else:
            self.button.setEnabled(False)

        self.values = newText

    def setButtonIcon(self, frame):
        '''Get the current state of the loading indicator gif as an icon'''
        icon = QtGui.QIcon(self.movie.currentPixmap())
        self.button.setIcon(icon)

    def submit(self):
        '''
            Send the selected values to a function set up in the calling class and
            close the window. Use connect() on submitted to set up the receiving func.
        '''
        print('comment input: ' + self.values + '\n')
        self.button.setText("Loading...")
        icon_path = os.path.join(env().project_dir, "pipe", "tools", "_resources", "loading_indicator_transparent.gif")
        self.movie = QtGui.QMovie(icon_path)
        self.movie.frameChanged.connect(self.setButtonIcon)
        if not self.movie.loopCount() == -1:
            self.movie.finished().connect(self.movie.start())
        self.movie.start()
        self.button.setEnabled(False)
        self.submitted.emit(self.values)
        self.close()


class VersionWindow(QtWidgets.QMainWindow):
    '''
    I don't think this was ever used.
    '''

    def __init__(self, parent):  # =hou.qt.mainWindow()):
        super(VersionWindow, self).__init__(parent)
        # you're going to have to set the parent explicitly when you call this function
        # because importing hou raises an error when this runs in maya

        # Function to build the UI
        # Create main widget
        main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(main_widget)

        # Initialize the layout
        global_layout = QtWidgets.QVBoxLayout()
        layout = QtWidgets.QFormLayout()
        main_widget.setLayout(global_layout)

        # Create Controls - Display Current Version
        self.current_version_label = QtWidgets.QLabel()
        self.current_version_label.setMinimumWidth(300)
        # Create Controls - Display Library Path
        self.current_path_label = QtWidgets.QLabel()
        # Create Controls - Display Divider
        line = QtWidgets.QFrame()
        line.setFrameStyle(QtWidgets.QFrame.HLine |
                           QtWidgets.QFrame.Sunken)
        # Create Controls - Major version int editor
        self.major_version = QtWidgets.QSpinBox()
        # Create Controls - Minor version int editor
        self.minor_version = QtWidgets.QSpinBox()
        # Create Controls - custom spin box that supports a zero padded syntax for integers (001 instead of 1)
        self.revision_version = PaddedSpinBox()
        # Create Controls - Create New Version button
        self.set_version = QtWidgets.QPushButton(
            'Create New Version')

        # Add controls to layout and set label
        layout.addRow('Current Version:', self.current_version_label)
        layout.addRow('Library Path:', self.current_path_label)
        layout.addRow(line)
        layout.addRow('Major Version:', self.major_version)
        layout.addRow('Minor Version:', self.minor_version)
        layout.addRow('Revision Version:', self.revision_version)

        # Global layout setting
        global_layout.addLayout(layout)
        global_layout.addWidget(self.set_version)


# PySide2 UI - custom QSpinBox that supports a zero padded syntax
# Subclass PySide2.QtWidgets.QSpinBox
class PaddedSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent=None):
        super(PaddedSpinBox, self).__init__(parent)

    # Custom format of the actual value returned from the text
    def valueFromText(self, text):
        regExp = QtCore.QRegExp(("(\\d+)(\\s*[xx]\\s*\\d+)?"))

        if regExp.exactMatch(text):
            return regExp.cap(1).toInt()
        else:
            return 0

    # Custom format of the text displayed from the value
    def textFromValue(self, value):
        return str(value).zfill(3)


def large_input(label, title='Input', text=None):
    '''
    Allows the user to respond with a larger text input
    If the okay button is pressed it returns the inputed text, otherwise None
    '''

    dialog = QtWidgets.QTextEdit()
    # dialog.setCancelButtonText("Skip")toPlainText
    text = dialog.toPlainText(None, title, label, text=text)

    if text[1]:
        return text[0]
    else:
        return None


def binary_option(text, optionOne, optionTwo, title='Question'):
    '''Gives the user a message and a binary choice'''
    '''returns True if option one is selected, false if the second option is selected, otherwise None'''
    msgBox = QtWidgets.QMessageBox()
    msgBox.setText(msgBox.tr(text))
    msgBox.setIcon(QtWidgets.QMessageBox.Question)
    msgBox.setWindowTitle(title)
    fristButton = msgBox.addButton(
        msgBox.tr(optionOne), QtWidgets.QMessageBox.ActionRole)
    secondButton = msgBox.addButton(
        msgBox.tr(optionTwo), QtWidgets.QMessageBox.ActionRole)
    cancelButton = msgBox.addButton(QtWidgets.QMessageBox.Cancel)

    msgBox.exec_()

    if msgBox.clickedButton() == fristButton:
        return True
    elif msgBox.clickedButton() == secondButton:
        return False
    return None


class CheckboxSelect(QtWidgets.QDialog):

    submitted = QtCore.Signal(list)

    def __init__(self, text, options, title="", parent=None):
        '''Creates check box options based on the given list of strings'''
        '''returns a list of booleans, each one correstponding to its respective option'''
        super(CheckboxSelect, self).__init__(parent=parent)

        # window = QtWidgets.QDialog(parent=parent)
        # self.setWindowTitle(title)

        self.layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel()
        label.setText(text)
        self.layout.addWidget(label)

        self.boxes = []

        for option in options:
            print(option)
            newBox = QtWidgets.QCheckBox()
            newBox.setText(option)
            newBox.setChecked(True)
            self.boxes.append(newBox)
            self.layout.addWidget(newBox)

        self.initializeSubmitButton()

        self.setLayout(self.layout)
        self.show()

    def initializeSubmitButton(self):
        self.button = QtWidgets.QPushButton("Accept")
        self.button.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.button.clicked.connect(self.submit)
        self.layout.addWidget(self.button)

    def submit(self):
        values = []
        for box in self.boxes:
            values.append(box.isChecked())
        self.submitted.emit(values)
        self.close()


def save(text):
    '''Prompts the user to save'''
    '''returns True if save is selected, False if don't save is selected otherwise None'''
    return binary_option(text, 'Save', 'Don\'t Save', title='Save Changes')
