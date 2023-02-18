import maya.cmds as cmds
import json
import os
import shutil
import functools
import time

from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Environment as umEnv
from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Element as umEl


class ShotCheckout:
    """This class holds required functions to check out shots in Maya"""

    def __init__(self):
        pass
        # self.run()

    def run(self):
        self.curr_env = umEnv.UnMaya_Environment()
        # Get shot list
        self.shot_list = self.curr_env.get_shot_list()
        self.shot_list = sorted(self.shot_list)
        self.check_save_state()

    def check_save_state(self):
        """Checks if the current scene has any unsaved changes, and prompts user to save or not"""
        unSaved = cmds.file(q=True, modified=True)
        if unSaved:
            print("Current Scene not saved")
            mes = "There are unsaved changes to the current file"
            confirm = cmds.confirmDialog(title='WARNING', message=mes, button=['Save and Continue',
                                         'Continue without Saving', 'Cancel'], defaultButton='Save and Continue',
                                         dismissString='Cancel')

            if confirm == "Save and Continue":
                cmds.SaveScene()
                self.check_save_state()
            elif confirm == "Continue without Saving":
                self.checkout_gui()
            else:
                pass

        else:
            self.checkout_gui()

    def getSelected(self, scrollList):
        """Receives a textScrollList and returns the currently selected list item"""
        selected = cmds.textScrollList(scrollList, q=1, si=1)
        return selected

    def checkout_gui(self):
        """GUI: displays a list of shots to select from"""

        import pipe.pipeHandlers.quick_dialogs as qd

        dialog = qd.ShotSelectDialog()

        if dialog.exec_():
            self.open_file(dialog.selectedShot())

    def open_file(self, selected_shot):
        """Opens the shot selected in the GUI"""
        try:
            print("Selected shot: ", selected_shot)
            # Get the .mb directory
            mb_dir = self.curr_env.get_mb_dir(selected_shot)
            print(f"mb_dir: {mb_dir}")
            # Access the respective .element file
            el = umEl.UnMaya_Element(mb_dir)
            # Check if the .mb file is already assigned
            if (el.is_assigned() is True):
                # If the .mb is already assigned, check if it is by the same user.
                assigned_user = el.get_assigned_user()
                if (el.get_assigned_user() != self.curr_env.get_username()):
                    response_text = "This shot is already checked out by: " + assigned_user
                    # If not, decline the users request
                    cmds.confirmDialog(message=response_text, button=["ok"])
                    # Reopen the checkout menu
                    self.checkout_gui()
                    return
            # If the user is the assigned user, or there is no assigned user, assign
            #  the user to the .element file
            el.assign_user(self.curr_env.get_username())
            # Write the .element file to disk
            el.write_element_file()
            # open the .mb file
            cmds.file(mb_dir, open=True, force=True)

            if cmds.window("ms_checkout_GUI", exists=True):
                cmds.deleteUI("ms_checkout_GUI")
        except RuntimeError as e:
            confirm = cmds.confirmDialog(title='WARNING', message=e, button=['Ok'], defaultButton='Ok',
                                         dismissString='Other')
            if confirm == "Ok":
                pass

    def search(self):
        """Supports the checkout gui by implementing a search function"""
        searchEntry = cmds.textFieldGrp('search_field', q=True, text=True)
        cmds.textScrollList("Shot_List", edit=True, removeAll=True)

        tempList = []
        for element in self.shot_list:
            if searchEntry.lower() in element.lower():
                tempList.append(element)
        cmds.textScrollList("Shot_List", edit=True, append=tempList)

    def base_list(self):
        """Supports the checkout by clearing the search function and returning to the base list"""
        cmds.textScrollList("Shot_List", edit=True, removeAll=True)
        cmds.textScrollList("Shot_List", edit=True, append=self.shot_list)
        cmds.textFieldGrp('search_field', edit=True, text="")
