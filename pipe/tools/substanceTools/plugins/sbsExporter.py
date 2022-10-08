from PySide2 import QtWidgets
import substance_painter.ui

plugin_widgets = []
"""Keep track of added ui elements for cleanup"""


def start_plugin():
    """This method is called when the plugin is started."""
    menu = QtWidgets.QMenu("UnPipe")
    action = QtWidgets.QAction("Publish", menu)
    action.triggered.connect(print_text)

    menu.addAction(action)
    substance_painter.ui.add_menu(menu)
    plugin_widgets.append(menu)
    print("This is in the pipe now")


def print_text():
    print("Hello from python scripting!")


def close_plugin():
    """This method is called when the plugin is stopped."""
    # We need to remove all added widgets from the UI.
    for widget in plugin_widgets:
        substance_painter.ui.delete_ui_element(widget)
    plugin_widgets.clear()


if __name__ == "__main__":
    print("Please work from here")
    start_plugin()
