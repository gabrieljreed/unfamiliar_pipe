from pipe.pipeHandlers.environment import Environment as env
import pipe.pipeHandlers.gui as gui
from pipe.pipeHandlers.element import Element

import nuke


class ShotCheckout:
    """This class holds required functions to check out shots in Nuke"""

    def __init__(self):
        # Get shot list
        self.shot_list = env().get_shot_list()

    def checkout(self):
        """Starts the gui for checking out shots"""
        # Open gui to select shot file
        self.filePath = nuke.getFilename('Select a shot to checkout', '*.txt *.xml')

        # Intilize gui with the shot list
        # self.item_gui = gui.SelectFromList(l=self.shot_list, parent=hou.ui.mainQtWindow(), title="Select a shot to checkout")
        # Send results from gui to the results method
        # self.item_gui.submitted.connect(self.results)

    def results(self, value):
        """Called after the user interacts with the gui"""
        print("Selected shot: " + value[0])
        # Get the hip directory
        hip_dir = env().get_hip_dir(value[0])
        # Access the respective .element file
        el = Element(hip_dir)
        # Check if the .hip file is already assigned
        if el.is_assigned():
            # If the .hip is already assigned, check if it is by the same user.
            if (el.get_assigned_user() != env().get_username()):
                # If not, decline the users request
                hou.ui.displayMessage("Shot is checked out by: " + el.get_assigned_user())
                # Reopen the checkout menu
                self.checkout()
                return

        # If the user is the assigned user, or there is no assigned user, assign
        # the user to the .elemnet file
        el.assign_user(env().get_username())
        # Write the .element file to disk
        el.write_element_file()
        # open the .hip file
        hou.hipFile.load(hip_dir)
