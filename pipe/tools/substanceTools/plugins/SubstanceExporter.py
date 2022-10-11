from PySide2 import QtWidgets
import substance_painter.ui
import os
import sys
sys.path.append(r"G:\unfamiliar\anim_pipeline")
import pipe.pipeHandlers.environment as unEnv

plugin_widgets = []
"""Keep track of added ui elements for cleanup"""


def start_plugin():
    """This method is called when the plugin is started."""
    menu = QtWidgets.QMenu("UnPipe")
    action = QtWidgets.QAction("Publish", menu)
    action.triggered.connect(launch_exporter)

    menu.addAction(action)
    substance_painter.ui.add_menu(menu)
    plugin_widgets.append(menu)


class SubstanceExporterWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SubstanceExporterWindow, self).__init__(parent)

        Env = unEnv.Environment()
        self.assets = Env.get_asset_list()

        self.assetsDir = r"G:\unfamiliar\anim_pipeline\production\assets"

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Unbstance Exporter")
        self.resize(400, 300)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.topLabel = QtWidgets.QLabel("Select an asset to publish textures for:")
        self.mainLayout.addWidget(self.topLabel)

        self.searchWidget = QtWidgets.QWidget()
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchWidget.setLayout(self.searchLayout)
        self.mainLayout.addWidget(self.searchWidget)

        # Add a search box 
        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search")
        self.searchBox.textChanged.connect(self.search)
        self.searchBox.resize(100, 20)
        self.searchLayout.addWidget(self.searchBox)

        # Add a clear button to the search box 
        self.clearButton = QtWidgets.QPushButton("X")
        self.clearButton.clicked.connect(self.searchBox.clear)
        self.clearButton.setFixedHeight(20)
        self.clearButton.setFixedWidth(20)
        self.clearButton.resize(20, 20)
        self.searchLayout.addWidget(self.clearButton)

        # Add a list widget to the dialog
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(self.assets)
        self.mainLayout.addWidget(self.list_widget)

        # Add a button to the dialog
        self.button = QtWidgets.QPushButton("Publish")
        self.button.clicked.connect(self.publish)
        self.mainLayout.addWidget(self.button)
    
    def search(self):
        search_term = self.searchBox.text()
        self.list_widget.clear()
        self.list_widget.addItems([asset for asset in self.assets if search_term in asset])

    def publish(self):
        # If there is no selected asset, return
        if not self.list_widget.selectedItems():
            return

        selected_asset = self.list_widget.currentItem().text()
        print(selected_asset)
        assetDir = os.path.join(self.assetsDir, selected_asset, "kljh")
        if not os.path.exists(assetDir):
            QtWidgets.QMessageBox.warning(self, "Asset not found", "The asset you selected doesn't exist. Please select a valid asset.")
            return
        
        texturesDir = os.path.join(assetDir, "materials", "textures")
        if not os.path.exists(texturesDir):
            os.makedirs(texturesDir)


        # Change permissions 
        for root, dirs, files in os.walk(assetDir):
            for file in files:
                try:
                    os.chmod(os.path.join(root, file), 0o777)
                except Exception as e:
                    print("Unable to change permissions on file: {}".format(os.path.join(root, file)))


def launch_exporter():
    # Check for existing windows and close them before opening a new one
    for widget in plugin_widgets:
        if isinstance(widget, SubstanceExporterWindow):
            widget.close()
            substance_painter.ui.delete_ui_element(widget)
            plugin_widgets.remove(widget)
            break

    window = SubstanceExporterWindow()
    substance_painter.ui.add_dock_widget(window)
    plugin_widgets.append(window)

    print("Launching Substance Exporter")

    # dialog = QtWidgets.QDialog()
    # dialog.setWindowTitle("Substance Exporter")
    # dialog.resize(400, 300)

    # if dialog.exec_():
    #     print("Dialog accepted")
    # else:
    #     print("Dialog rejected")


def close_plugin():
    """This method is called when the plugin is stopped."""
    # We need to remove all added widgets from the UI.
    print("Closing Substance Exporter")
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()


if __name__ == "__main__":
    print("Please work from here")
    start_plugin()