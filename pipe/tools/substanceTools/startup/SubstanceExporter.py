from PySide2 import QtWidgets, QtCore

import substance_painter.ui
import substance_painter.export
import substance_painter.project
import substance_painter.textureset

import os
import sys
sys.path.append(r"G:\unfamiliar\anim_pipeline")

import pipe.pipeHandlers.environment as unEnv
import pipe.pipeHandlers.permissions as permissions

plugin_widgets = []
window = None
"""Keep track of added ui elements for cleanup"""


def start_plugin():
    """This method is called when the plugin is started."""
    print("Plugin started")
    menu = QtWidgets.QMenu("UnPipe")
    action = QtWidgets.QAction("Publish", menu)
    action.triggered.connect(launch_exporter)

    menu.addAction(action)
    substance_painter.ui.add_menu(menu)
    plugin_widgets.append(menu)


class SubstanceExporterWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SubstanceExporterWindow, self).__init__(parent)

        Env = unEnv.Environment()
        self.assets = Env.get_asset_list()

        self.assetsDir = Env.get_asset_dir()

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Unbstance Exporter")
        self.resize(400, 300)

        # Make sure the window always stays on top
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.mainLayout)

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
        self.searchBox.setFixedHeight(50)
        self.searchLayout.addWidget(self.searchBox)

        # Add a clear button to the search box 
        self.clearButton = QtWidgets.QPushButton()
        self.clearButton.setText("Clear")
        self.clearButton.clicked.connect(self.searchBox.clear)
        self.clearButton.setFixedWidth(2)
        self.clearButton.setStyleSheet("padding: 0px; margin: 0px;")
        self.searchLayout.addWidget(self.clearButton)

        # Add a list widget to the dialog
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setStyleSheet("QListWidget {background-color: #202020; color: #ffffff;}")
        self.list_widget.addItems(self.assets)
        self.mainLayout.addWidget(self.list_widget)

        # Add a combo box to the dialog 
        self.texture_size_label = QtWidgets.QLabel("Texture size:")
        self.mainLayout.addWidget(self.texture_size_label)

        self.size_combo_box = QtWidgets.QComboBox()
        self.size_combo_box.addItems(["128", "256", "512", "1024", "2048", "4096", "8192"])
        self.size_combo_box.setCurrentText("2048")
        self.mainLayout.addWidget(self.size_combo_box)

        # Add a button to the dialog
        self.buttonBox = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton("Publish")
        self.button.clicked.connect(self.publish)
        self.buttonBox.addWidget(self.button)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        self.buttonBox.addWidget(self.cancelButton)

        self.mainLayout.addLayout(self.buttonBox)

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
        assetDir = os.path.join(self.assetsDir, selected_asset)
        if not os.path.exists(assetDir):
            print(f"Asset directory {assetDir} does not exist")
            QtWidgets.QMessageBox.warning(self, "Asset not found", "The asset you selected doesn't exist. Please select a valid asset.")
            return

        texturesDir = os.path.join(assetDir, "materials", "textures")
        if not os.path.exists(texturesDir):
            os.makedirs(texturesDir)
            # Set permissions on the folder
            permissions.set_permissions(texturesDir)

        # Export textures
        self.export_textures(export_path=texturesDir)

        # Change permissions
        permissions.set_permissions(assetDir)

    def export_textures(self, export_path=None):
        if not substance_painter.project.is_open():
            QtWidgets.QMessageBox.warning(self, "No project open", "Please open a project before exporting textures.")
            return

        # Get the currently active layer stack (paintable)
        stack = substance_painter.textureset.get_active_stack()

        material = stack.material()

        # TODO: Replace these with relative paths
        resource_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "resources"))
        PBRMR_preset = substance_painter.resource.import_project_resource(os.path.join(resource_dir, "PBRMR.spexp"),
            substance_painter.resource.Usage.EXPORT)

        RMAN_preset = substance_painter.resource.import_project_resource(os.path.join(resource_dir, "RMAN.spexp"),
            substance_painter.resource.Usage.EXPORT)

        resolution = material.get_resolution()

        Path = export_path
        if not Path.endswith("/"):
            Path += "/"

        PBRMR_config = {
            "exportShaderParams" 	: False,
            "exportPath" 			: Path,
            "exportList"			: [ { "rootPath" : str(stack) } ],
            "exportPresets" 		: [ { "name" : "default", "maps" : [] } ],
            "defaultExportPreset" 	: PBRMR_preset.identifier().url(),
            "exportParameters" 		: [
                {
                    "parameters"	: 
                        {
                            "paddingAlgorithm": "infinite" ,
                            "sizeLog2" : self.size_combo_box.currentIndex() + 7,
                        }
                    }
            ]
        }

        RMAN_config = {
            "exportShaderParams" 	: False,
            "exportPath" 			: Path,
            "exportList"			: [ { "rootPath" : str(stack) } ],
            "exportPresets" 		: [ { "name" : "default", "maps" : [] } ],
            "defaultExportPreset" 	: RMAN_preset.identifier().url(),
            "exportParameters" 		: [
                {
                    "parameters"	: 
                        { 
                            "paddingAlgorithm": "infinite",
                            "sizeLog2" : self.size_combo_box.currentIndex() + 7,
                        }
                }
            ]
        }

        error = False

        try:
            substance_painter.export.export_project_textures(PBRMR_config)
            print(f"Exported PBRMR textures to {Path}")
        except Exception as e:
            error = True
            print(e)
            QtWidgets.QMessageBox.warning(self, "Error",
            "An error occurred while exporting PBRMR textures. Please check the console for more information.")

        try:
            substance_painter.export.export_project_textures(RMAN_config)
            print(f"Exported RMAN textures to {Path}")
        except Exception as e:
            error = True
            print(e)
            QtWidgets.QMessageBox.warning(self, "Error",
            "An error occurred while exporting RMAN textures. Please check the console for more information.")

        # Change permissions
        permissions.set_permissions(Path)

        if error:
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while exporting textures. Please check the console for more information.")
            return
        QtWidgets.QMessageBox.information(self, "Export complete", "Textures exported successfully.")


def launch_exporter():
    # Check for existing windows and close them before opening a new one
    for widget in plugin_widgets:
        if isinstance(widget, SubstanceExporterWindow):
            widget.close()
            substance_painter.ui.delete_ui_element(widget)
            plugin_widgets.remove(widget)
            break

    global window
    window = SubstanceExporterWindow()
    window.show()
    # substance_painter.ui.add_dock_widget(window)
    # plugin_widgets.append(window)

    print("Launching Substance Exporter")


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
