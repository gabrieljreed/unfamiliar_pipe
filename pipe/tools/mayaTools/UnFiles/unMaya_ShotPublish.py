import maya.cmds as cmds
import json
import os, shutil, functools, time

from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Environment as umEnv
from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Element as umEl

#This class publishes the shot back to the pipe. This includes version control
class UnMaya_ShotPublish:
    
      
    def __init__(self):
        pass 
        #self.run()       
    
    #Gets shot list and starts the gui  
    def run(self):
        #Get shot list
        self.curr_env = umEnv.UnMaya_Environment()
        self.shot_list = self.curr_env.get_shot_list()
        self.shot_list = sorted(self.shot_list)
        self.select_shot_gui()
    
    #Receives a textScrollList and returns the currently selected list item
    def getSelected(self, scrollList):
        selected = cmds.textScrollList(scrollList, q=1, si=1)
        return selected
    
    #GUI: Displays a list of all the shots to select and publish
    def select_shot_gui(self):
        
        if cmds.window("ms_publish_GUI", exists=True):
            cmds.deleteUI("ms_publish_GUI")

        win = cmds.window("ms_publish_GUI", title="PUBLISH SHOT") 
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
        #Button to select the shot that is currently open
        cmds.button(label="Select Current Shot", c=lambda x: self.select_current_shot(selection))
        #Button to publish the selected shot
        cmds.button(label="Publish Shot", c=lambda x: self.publish(self.getSelected(selection)))
        cmds.setParent("..")
        
    def select_current_shot(self, scrollList):
        
        #Gets name of current shot
        fullNamePath = cmds.file( q =1, sn = 1)
        dirPath = os.path.dirname(fullNamePath)
        shotName = dirPath.split('/')[-1]
       
        #Sets the selection to the currently opened shot
        cmds.textScrollList( "Shot_List", edit=True, selectItem=shotName)
        
    #Publishes given shot, including setting the element file, and starting the comment gui 
    def publish(self, shotToPublish):
        self.selectedShot = shotToPublish[0]
        print("Selected Shot: ", self.selectedShot)
        mb_dir = self.curr_env.get_mb_dir(self.selectedShot)
        self.el = umEl.UnMaya_Element(mb_dir)
        self.comment_gui()
    
    #GUI: gets comment from current user about current publish version  
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

        # Prefix and Suffix boxes
        cmds.rowLayout(nc=1)
        self.prefix = cmds.textFieldGrp('comment', label='Comment:')
        cmds.setParent('..')


        # Create export button
        cmds.columnLayout(adjustableColumn=True, columnAlign='center')
        cmds.button(label='Publish', command=lambda x: self.comment_results())
        cmds.setParent('..')
        cmds.showWindow(self.window)
        
    #Gets comment, versions the file and updates the .element file    
    def comment_results(self):
        self.comment = cmds.textFieldGrp('comment', q=True, text=True)
        self.version_file()
        self.update_element_file()
        
        if cmds.window('msCommentWindowID', exists=True):
            cmds.deleteUI('msCommentWindowID')
            
        if cmds.window('ms_publish_GUI', exists=True):
            cmds.deleteUI('ms_publish_GUI')
    
    #Returns the name of the current file
    def get_fileName(self):
        fullNamePath = cmds.file( q=1, sn = 1)
        fileName_withExt = fullNamePath.split('/')[-1]
        fileName = fileName_withExt.split('.')[0]
        return fileName
    
    #Saves and versions the file    
    def version_file(self):
        #Save current file
        cmds.file(save = True)
        #Get new version number
        self.ver_num = self.el.get_latest_version() + 1
        dir_name = ".v" + f"{self.ver_num:04}"
        
        curr_fileName = self.get_fileName()
        dest_fileName = self.selectedShot + "_main"
        
        #Make hidden directory with version number
        new_dir_path = os.path.join(self.curr_env.get_file_dir(self.el.filepath), dir_name)
        os.mkdir(new_dir_path)
        try:
            os.chmod(new_dir_path, mode=0o777)
        except Exception as e:
            print("Unable to change permissions on version directory")
        
        #If current file is not the shot file, then copy the current file into the shot_main of the new shot
        if curr_fileName != dest_fileName:
            curr_filePath = cmds.file( q=1, sn=1) 
            print("current filepath:", curr_filePath)
            print("new dir path:", self.el.filepath)
            shutil.copy(curr_filePath, self.el.filepath)
            try:
                os.chmod(self.el.filepath, mode=0o777)
            except Exception as e:
                print("Unable to change permissions on shot file")
        
        #Copy current .mb file into new directory and rename it
        new_file_path = new_dir_path + '/' + self.el.get_file_parent_name() + self.el.get_file_extension()
        shutil.copy(self.el.filepath, new_file_path)
            
    #Updates the element file with the comment, version number, and also removes the current assigned user
    def update_element_file(self):
        #Adds new publish log to list of publishes
        self.comment = "v" + str(self.ver_num) + ": " + self.comment
        self.el.add_publish_log(self.comment)
        #Set latest version
        self.el.set_latest_version(self.ver_num)
        #Remove assigned user
        self.el.assign_user('')
        #Write the .element file to disk
        self.el.write_element_file()
    
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
