import maya.cmds as cmds
import json
import os, shutil, functools, time

from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Environment as umEnv
from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Element as umEl

#This class holds required functions to check out shots in Maya
class ShotCheckout:
    
    def __init__(self):
        pass
        #self.run()    
    
    def run(self):
        self.curr_env = umEnv.UnMaya_Environment()
        #Get shot list
        self.shot_list = self.curr_env.get_shot_list()
        self.shot_list = sorted(self.shot_list)
        self.checkout_gui()
    
     #Receives a textScrollList and returns the currently selected list item
    def getSelected(self, scrollList):
        selected = cmds.textScrollList(scrollList, q=1, si=1)
        return selected
    
    #GUI: displays a list of shots to select from
    def checkout_gui(self):
        if cmds.window("ms_checkout_GUI", exists=True):
            cmds.deleteUI("ms_checkout_GUI")

        win = cmds.window("ms_checkout_GUI", title="CHECKOUT SHOT") 
        cmds.showWindow(win)
        cmds.columnLayout()
        
        cmds.rowLayout(nc=3)
        self.prefix = cmds.textFieldGrp('search_field')
        cmds.button(label="Search", c=lambda x: self.search())
        cmds.button(label="X", c=lambda x: self.base_list())
        cmds.setParent('..')
        
        selection = cmds.textScrollList( "Shot_List", numberOfRows=8,
		        	append=self.shot_list,
			        selectIndexedItem=1, showIndexedItem=1)
        
        cmds.rowLayout(numberOfColumns=1)
        #Button to open the selected shot
        cmds.button(label="Checkout Shot", c=lambda x: self.open_file(self.getSelected(selection)))
        cmds.setParent("..")
    
    #Opens the shot selected in the GUI    
    def open_file(self, selected_shot):
        
        try:
            print("Selected shot: ", selected_shot[0])
            #Get the .mb directory
            mb_dir = self.curr_env.get_mb_dir(selected_shot[0])
            #Access the respective .eleent file
            el = umEl.UnMaya_Element(mb_dir)
            #Check if the .mb file is already assigned
            if (el.is_assigned() == True):
                #If the .mb is already assigned, check if it is by the same user.
                assigned_user = el.get_assigned_user()
                if (el.get_assigned_user() != self.curr_env.get_username()):
                    response_text = "This shot is already checked out by: " + assigned_user
                    #If not, decline the users request
                    cmds.confirmDialog(message=response_text, button=["ok"])
                    #Reopen the checkout menu
                    self.checkout_gui()
                    return
            #If the user is the assigned user, or there is no assigned user, assign
            #  the user to the .element file
            el.assign_user(self.curr_env.get_username())
            #Write the .element file to disk
            el.write_element_file()
            #open the .mb file
            cmds.file(mb_dir, open=True)
            
            if cmds.window("ms_checkout_GUI", exists=True):
                cmds.deleteUI("ms_checkout_GUI")
        except RuntimeError as e:
            confirm = cmds.confirmDialog ( title='WARNING', message=e, button=['Ok'], defaultButton='Ok', dismissString='Other' )
            if confirm == "Ok":
                pass

        #Supports the checkout gui by implementing a search function
    def search(self):
        searchEntry = cmds.textFieldGrp('search_field', q=True, text=True)
        cmds.textScrollList( "Shot_List", edit=True, removeAll=True)
            
        tempList = []
        for element in self.shot_list:
            if searchEntry.lower() in element.lower():
                tempList.append(element)
        cmds.textScrollList( "Shot_List", edit=True, append=tempList)
    
    #Supports the checkout by clearing the search function and returning to the base list        
    def base_list(self):
        cmds.textScrollList( "Shot_List", edit=True, removeAll=True)
        cmds.textScrollList( "Shot_List", edit=True, append=self.shot_list)
        cmds.textFieldGrp('search_field', edit=True, text="")  

#ShotCheckout()
