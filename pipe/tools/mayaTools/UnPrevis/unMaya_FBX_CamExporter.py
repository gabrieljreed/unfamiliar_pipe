import maya.cmds as cmds
from pathlib import Path
import os, shutil
import maya.mel as mel

from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Element as umEl
from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Environment as umEnv

class Camera_Exporter:
    def __init__(self):
        #self.run()
        pass  
    
    def run(self):
        self.CAM_DIR = "camera"
        self.SHOTS_DIR = "/groups/unfamiliar/anim_pipeline/production/shots"
        
        self.curr_env = umEnv.UnMaya_Environment()
        self.check_if_selected()
    
    #Checks if here is something selected in the scene. If there is, it continues to the shot_select_gui
    def check_if_selected(self):
        curr_selection = cmds.ls(selection=True)
        if len(curr_selection) == 0:
            confirm = cmds.confirmDialog ( title='WARNING', message="Nothing is selected", button=['Ok'], defaultButton='Ok', dismissString='Other' )
            if confirm == "Ok":
                pass
        else:
            self.shot_select_gui()
            
    
    #GUI to select which shot you are exporting the camera from    
    def shot_select_gui(self):
        self.shot_list = self.curr_env.get_shot_list_undef(self.SHOTS_DIR)
        self.shot_list = sorted(self.shot_list)
        
        if cmds.window("ms_selectShot_GUI", exists=True):
                cmds.deleteUI("ms_selectShot_GUI")

        win = cmds.window("ms_selectShot_GUI", title="SELECT SHOT GUI") 
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
        
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="Select Current Shot", c=lambda x: self.select_current_shot(selection))
        cmds.button(label="Next", c=lambda x: self.save_shot(self.getSelected(selection)[0]))
        cmds.setParent("..")
    
    #Supports the Shot select gui by implementing a search function
    def search(self):
        searchEntry = cmds.textFieldGrp('search_field', q=True, text=True)
        cmds.textScrollList( "Shot_List", edit=True, removeAll=True)
            
        tempList = []
        for element in self.shot_list:
            if searchEntry.lower() in element.lower():
                tempList.append(element)
        cmds.textScrollList( "Shot_List", edit=True, append=tempList)
    
    #Supports the Shot selection by clearing the search function and returning to the base list        
    def base_list(self):
        cmds.textScrollList( "Shot_List", edit=True, removeAll=True)
        cmds.textScrollList( "Shot_List", edit=True, append=self.shot_list)
        cmds.textFieldGrp('search_field', edit=True, text="")  
    
    def select_current_shot(self, scrollList):
        
        fullNamePath = cmds.file( q =1, sn = 1)
        dirPath = os.path.dirname(fullNamePath)
        shotName = dirPath.split('/')[-1]
        print(fullNamePath, dirPath, shotName)
       
        if shotName in self.shot_list:
            #Sets the selection to the currently opened shot
            cmds.textScrollList( scrollList, edit=True, selectItem=shotName)
        else: 
            confirm = cmds.confirmDialog ( title='WARNING', message="The current Maya file is not in the shot list", button=['Ok'], defaultButton='Ok', dismissString='Other' )
            if confirm == "Ok":
                pass
        
    #Receives a textScrollList and returns the currently selected list item
    def getSelected(self, scrollList):
        selected = cmds.textScrollList(scrollList, q=1, si=1)
        return selected
    
    def save_shot(self, selected_shot):
        self.shot_selection = selected_shot
        
        if cmds.window("ms_selectShot_GUI", exists=True):
                cmds.deleteUI("ms_selectShot_GUI")
                
        self.trigger_exportFBX()
    
    #Creates the fbx_filepath, checks if the camera file exists in the shot directory, makes it if not. Triggers versioning and comment_gui            
    def trigger_exportFBX(self):
        
        self.fbx_filepath = self.SHOTS_DIR + "/" + self.shot_selection + "/" + self.CAM_DIR 
        
        if not self.dir_exists(self.fbx_filepath):
            os.mkdir(self.fbx_filepath)
        
        command = self.get_fbx_command(self.fbx_filepath)    
        self.el = umEl.UnMaya_Element(self.fbx_filepath)
        self.version_fbx(command)
        self.comment_gui()

    #Checks if a dir exists, returns True or False 
    def dir_exists(self, dir_path):
        my_file = Path(dir_path)
        return my_file.is_dir()
     
    #Gets the commands needed for an fbx export. Sets the file name. Updates the self.fbx_filepath with file name       
    def get_fbx_command(self, file_path):
        save_name = file_path + "/camera_main" 
        command = "FBXExport -f \"" + save_name + "\" -s"
        self.fbx_filepath = save_name + ".fbx"
        return command 
    
    #Exports the FBX and versions it 
    def version_fbx(self, command):
        #Temporarily rename the camera for exportation
        ##old_cam_name = curr_selection = cmds.ls(selection=True)[0]
        ##cmds.rename(cmds.ls(selection=True)[0], self.shot_selection)
        #Export FBX to _main.fbx
        mel.eval(command)
        #Rename camera back to original name
        ##cmds.rename(cmds.ls(selection=True)[0], old_cam_name)
        
        #Get new version number
        self.ver_num = self.el.get_latest_version() + 1 
        dir_name = ".v" + f"{self.ver_num:04}"
        #Make hidden directory with version number
        new_dir_path = os.path.join(self.curr_env.get_file_dir(self.el.filepath), dir_name)
        os.mkdir(new_dir_path)
        #Copy FBX into the new directory and rename it
        new_file_path = new_dir_path + "/" + self.el.get_file_parent_name() + self.el.get_file_extension()
        shutil.copy(self.el.filepath, new_file_path)
        
            
    #updates the element file with the comment
    def update_element_file(self):
        #Adds new publish log to list of publishes
        self.comment = "v" + str(self.ver_num) + ": " + self.comment
        self.el.add_publish_log(self.comment)
        #Set latest version
        self.el.set_latest_version(self.ver_num)
        #Write the .element file to disk
        self.el.write_element_file()
    
    #GUI: Prompts the user to imput a comment for the current export
    def comment_gui(self):
        #Make list of past comments for the gui
        publishes = self.el.get_publishes_list()
        if len(publishes) > 10:
            publishes = publishes[-10:]
        publishes_list = []
        if len(publishes) != 0:
            for publish in publishes:
                label = publish[0] + ' ' + publish[1] + ' ' + publish[2] + '\n'
                publishes_list.insert(0, label)
                            
        # Make a new default window
        windowID = 'msCommentWindowID'
        
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

        self.window = cmds.window(windowID, title="Comment", sizeable=False, iconName='Short Name',
                                  resizeToFitChildren=True)

        cmds.rowColumnLayout(nr=5)
        cmds.textScrollList( "Publish_List", numberOfRows=8, append=publishes_list)

        # Comment Box
        cmds.rowLayout(nc=1)
        self.prefix = cmds.textFieldGrp('comment', label='Comment:')
        cmds.setParent('..')

        # Create export button
        cmds.columnLayout(adjustableColumn=True, columnAlign='center')
        cmds.button(label='Export', command=lambda x: self.comment_results())
        cmds.setParent('..')
        cmds.showWindow(self.window)  
                
    #Gets comment, updates the .element file with the comment    
    def comment_results(self):
        self.comment = cmds.textFieldGrp('comment', q=True, text=True)
        self.update_element_file()
        
        if cmds.window('msCommentWindowID', exists=True):
            cmds.deleteUI('msCommentWindowID')
        
        
#Camera_Exporter()
