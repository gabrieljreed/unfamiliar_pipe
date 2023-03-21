import maya.cmds as cmds
from pathlib import Path
import os, shutil
import maya.mel as mel

from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Element as umEl
from pipe.tools.mayaTools.UnMaya_PipeHandlers import unMaya_Environment as umEnv
import pipe.pipeHandlers.permissions as permissions


class Camera_Exporter:
    def __init__(self):
        #self.run()
        pass  
    
    def run(self):
        
        #Filepaths for storing the fbx for Houdini
        self.CAM_DIR = "camera"
        self.SHOTS_DIR = "/groups/unfamiliar/anim_pipeline/production/shots"
        
        #Filepaths for storing the fbx for Unreal   
        self.UNREAL_EXPORTS_FOLDER = self.get_fileName() + "_ExportsUE"
        self.PREVIS_SEQUENCE_FILEPATH = "/groups/unfamiliar/previs/SHOTS"
        
        
        self.curr_env = umEnv.UnMaya_Environment()
        self.check_if_selected()
    
    def get_fileName(self):
        fullNamePath = cmds.file( q=1, sn = 1)
        fileName_withExt = fullNamePath.split('/')[-1]
        fileName = fileName_withExt.split('.')[0]
        return fileName
    
    #Checks if here is something selected in the scene. If there is, it continues to the shot_select_gui, making sure that the shotCam's main layer is selected
    def check_if_selected(self):
        curr_selection = cmds.ls(selection=True)
        if len(curr_selection) == 0:
            confirm = cmds.confirmDialog ( title='WARNING', message="Nothing is selected", button=['Ok'], defaultButton='Ok', dismissString='Other' )
            if confirm == "Ok":
                pass
        else:
            split_names = curr_selection[0].split(':')
            if len(split_names) > 2:
                shotCam_name = ''
                for i in range(0,len(split_names)-1):
                    shotCam_name = shotCam_name + ':' + split_names[i]
            else:
                shotCam_name = curr_selection[0].split(':')[0]
            shotCam_main = shotCam_name + ':Main'            
            self.selected_cam = [shotCam_main]
            cmds.select(shotCam_main)
            self.shot_select_gui()
            

###############################################################
###                  SELECT SHOT FUNCTIONS                  ###          
    
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

        cmds.columnLayout(adjustableColumn=True, columnAlign='center')
        cmds.checkBox( 'unreal_shift', label='Shift Unreal camera animations to zero', value=True)
        cmds.setParent('..')
    
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
    
    #Saves the selected shot to the self.shot_selection variable and triggers the export function
    def save_shot(self, selected_shot):
        self.shot_selection = selected_shot
        
        self.unreal_shift = cmds.checkBox('unreal_shift', q=True, v=True)

        if cmds.window("ms_selectShot_GUI", exists=True):
                cmds.deleteUI("ms_selectShot_GUI")
        
                       
        self.set_houdini_filepath(True)            
        self.set_unreal_filepath(True)
        self.get_auto_frameRange() 


###############################################################
###                  FRAME RANGE FUNCTIONS                  ###
    
    
    #Works with the camera sequencer to find the frame range of the camera's shot    
    def get_auto_frameRange(self):
                
        sequence = cmds.listConnections("sequencer1", type="shot")
        if sequence != None:
            for curr_shot in sequence:
                shot_name = cmds.shot(curr_shot, q=True, shotName=True)
                if shot_name in self.shot_selection:
                    self.cam_shot = curr_shot
                    break
                else:
                    self.cam_shot = None
                
            if self.cam_shot != None:
                self.shot_start = int(cmds.shot(self.cam_shot, q=True, startTime=True))
                self.shot_end = int(cmds.shot(self.cam_shot, q=True, endTime=True))
                self.comment_gui()
            else:
                self.get_frameRange_gui()
        else:
            self.get_frameRange_gui()
        
    #GUI: Prompts for the first and last frame to export
    def get_frameRange_gui(self):
        # Make a new default window
        windowID = 'msFrameRangeWindowID'
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

        self.window = cmds.window(windowID, title="Select Frame Range", sizeable=False, iconName='Short Name',
                                  resizeToFitChildren=True)

        cmds.columnLayout( adjustableColumn=True )
        cmds.text( label='Unable to automatically find the shot\'s framerange. Please enter it manually.')

        cmds.rowColumnLayout(nr=5)

        # StartFrame and EndFram boxes
        cmds.rowLayout(nc=4)
        cmds.textFieldGrp('startFrame', label='Start Frame:')
        cmds.textFieldGrp('endFrame', label='End Frame:')
        cmds.setParent('..')
        cmds.separator(h=30, vis=True)

        # Create a Playback range button
        cmds.rowLayout(nc=1)
        cmds.button(label='Next', command=lambda x: self.get_manual_frameRange())
        cmds.setParent('..')
        cmds.showWindow(self.window)

    #Saves the frame range from the gui  
    def get_manual_frameRange(self):
        
        self.shot_start = cmds.textFieldGrp('startFrame', q=True, text=True)
        self.shot_end = cmds.textFieldGrp('endFrame', q=True, text=True)
        
        error_message = ""
        if not self.shot_start or not self.shot_end:
            error_message = "Entries can not be empty"
        elif not self.shot_start.isdigit():
            if self.shot_start[0] == '-' and self.shot_start[1:].isdigit():
                pass
            else:
                error_message = "Entries must be integers"
        elif not self.shot_end.isdigit():
            if self.shot_end[0] == '-' and self.shot_end[1:].isdigit():
                pass
            else:
                error_message = "Entries must be integers"
        elif self.shot_end < self.shot_start:
            error_message = "End frame must be greater than the start frame"
        
        if error_message != "":
            confirm = cmds.confirmDialog ( title='WARNING', message=error_message, button=['Ok'], defaultButton='Ok', dismissString='Other' )
            if confirm == "Ok":
                pass
        else:
            if cmds.window('msFrameRangeWindowID', exists=True):
                cmds.deleteUI('msFrameRangeWindowID')
            
            self.comment_gui()


###############################################################
###                 EXPORT CAM FUNCTIONS                    ###         
    
        
    #Checks if a dir exists, returns True or False 
    def dir_exists(self, dir_path):
        my_file = Path(dir_path)
        return my_file.is_dir() 

    #Initiates the exporter for houdini and unreal, as well as the comment gui
    def trigger_exports(self):
        self.exportFBX_houdini()
        if self.unreal_filepath != "nounreal":
            self.exportFBX_unreal()

    # Sets the self.houdini_filepath variable and creates the camera directory if it does not already exist
    def set_houdini_filepath(self, withFile):
        filepath = self.SHOTS_DIR + "/" + self.shot_selection + "/" + self.CAM_DIR

        if not self.dir_exists(filepath):
            os.mkdir(filepath)
            permissions.set_permissions(filepath)

        if withFile:
            self.houdini_filepath_noExt = filepath + "/camera_main"
            self.houdini_filepath = filepath + "/camera_main.fbx"
        else:
            self.houdini_filepath = filepath

    # Sets the self.unreal_filepath variablet
    def set_unreal_filepath(self, withFile):
        filepath = self.find_shot_file()
        if filepath == "nounreal":
            self.unreal_filepath = filepath
                
        if withFile:
            self.unreal_filepath_noExt = filepath + "/camera_main"
            self.unreal_filepath = self.unreal_filepath_noExt + ".fbx"
        else:
            self.unreal_filepath = filepath
    
    # Takes the selected shot and finds the subsequence folder under previs 
    def find_shot_file(self):
        print("Selected Shot:", self.shot_selection) 
        shot_sections = self.shot_selection.split('_')
        
        sequence_list = self.curr_env.get_shot_list_undef(self.PREVIS_SEQUENCE_FILEPATH)
        if "test" not in shot_sections and "render" not in shot_sections and "Issues" not in shot_sections:
            sequence_list = sorted(sequence_list)
            sequence_list = sequence_list[1:-1]
            
            folder_index = ord(shot_sections[0]) - 65
            sequence_dir = sequence_list[folder_index]
            curr_filepath = self.PREVIS_SEQUENCE_FILEPATH + "/" + sequence_dir
            
            subsequence_list = self.curr_env.get_shot_list_undef(curr_filepath)
            subsequence_list = sorted(subsequence_list)
            self.subsequence = ""
            for element in subsequence_list:
                try:
                    element_dict = self.split_subsequence_name(element)
                except:
                    continue 
                if element_dict["SEQ"] != "none":
                    if shot_sections[1] >= element_dict["START"]:
                        if shot_sections[1] <= element_dict["END"]:
                            self.subsequence = element
                            break
            
            print("sub:", self.subsequence)
            
            #inserts the export folder directory into the path
            curr_filepath = curr_filepath + "/" + self.subsequence + "/" + self.UNREAL_EXPORTS_FOLDER
            if not self.dir_exists(curr_filepath):
                os.mkdir(curr_filepath)
                permissions.set_permissions(curr_filepath)
            
            #inserts the "camera" directory into the path
            curr_filepath = curr_filepath + "/" + self.CAM_DIR
            if not self.dir_exists(curr_filepath):
                os.mkdir(curr_filepath)

                permissions.set_permissions(curr_filepath)

            #inserts the specific shot directory into the path
            curr_filepath = curr_filepath + "/" + self.shot_selection 
            if not self.dir_exists(curr_filepath):
                os.mkdir(curr_filepath)
                
                permissions.set_permissions(curr_filepath)
    
            return curr_filepath
        else:
            return "nounreal"
    
    # Takes the subsequence and splits into into a dictionary including the sequence, start shot and end shot
    def split_subsequence_name(self, subsequence):
        dict = {}
         
        temp = subsequence.split('_')
        if len(temp) < 2:
            dict["SEQ"] = "none"
            dict["START"] = "none"
            dict["END"] = "none"
        else:
            dict["SEQ"] = temp[0]
            temp = temp[1].split('-')
            dict["START"] = temp[0]
            dict["END"] = temp[1]
        
        return dict          
    
    # Duplicates the selected cam including keyframes
    def duplicate_cam(self):

        camera_name = self.shot_selection
        
        ##orig_cam = cmds.ls(selection=True)[0]
        orig_cam = self.selected_cam[0]
        full_origCam = [orig_cam]
        full_origCam.extend(cmds.listRelatives(orig_cam, allDescendents=True))
        
        cmds.duplicate(orig_cam, name=camera_name)
        
        new_cam = cmds.ls(selection=True)[0]
        self.new_houdini_cam = new_cam
        full_newCam = [new_cam]
        full_newCam.extend(cmds.listRelatives(new_cam, allDescendents=True))

        #Copies keyframes for each control on the camera
        index = 0
        for cam_piece in full_origCam:
            if cmds.keyframe(cam_piece, query=True, time=(self.shot_start, self.shot_end), keyframeCount=True) > 0:
                #Gets current keyframes and checks if there are any keyframes on the first and last frame of the shot
                curr_keyframes = cmds.keyframe(cam_piece, q=True)
                if self.shot_start in curr_keyframes:
                    start = True
                else:
                    start = False
                if self.shot_end in curr_keyframes:
                    end = True
                else:
                    end = False
                
                #Sets keyframes on the first and last frame of the shot
                cmds.setKeyframe(cam_piece, insert=True, t=[self.shot_start, self.shot_end])

                #Copies keyframes over to the other camera
                self.copy_keyframes(cam_piece, full_newCam[index])
                
                #Removes the start and end frame keyframes if they did not previously exist
                if not start:
                    cmds.cutKey( cam_piece, time=(self.shot_start, self.shot_start))
                if not end:
                    cmds.cutKey( cam_piece, time=(self.shot_end, self.shot_end)) 
            index += 1
    
    #copies the keyframes from one obj to another
    def copy_keyframes(self, old_cam, new_cam):
        
        start_time = int(self.shot_start)
        end_time = int(self.shot_end)
                
        cmds.copyKey( old_cam, time=(start_time,end_time) )
        
        offset = start_time * -1
        cmds.pasteKey( new_cam, timeOffset=offset)
    
    
    #Generates the camera for houdini element file, exports with the proper settings for houdini, and triggers the versioning function    
    def exportFBX_houdini(self):
        self.houdini_el = umEl.UnMaya_Element(self.houdini_filepath)
        command = "FBXExport -f \"" + self.houdini_filepath_noExt + "\" -s"
        
        #Duplicate camera, adjust keyframes in shot to start at 0, leave new cam selected
        self.duplicate_cam() 
        #new_cam = cmds.ls(selection=True)[0]
        new_cam = self.new_houdini_cam
        
        mel.eval(command)

        permissions.set_permissions(self.houdini_filepath)
        
        # delete duplicate camera
        cmds.select(new_cam)
        cmds.delete()
        
        #version houdini fbx file
        self.version(self.houdini_el)

    #returns the name of the camera's base ShotCam layer
    def get_shotCam(self, cam_selection):
        if "ShotCam_000" in cam_selection and "Shape" not in cam_selection:
            return cam_selection
        else:
            descendents = cmds.listRelatives(cam_selection, allDescendents=True)
            for sub in descendents:
                if "ShotCam_000" in sub and "Shape" not in sub:
                    return sub
        
    #Generates the camera for unreal element file, exports with the proper settings for houdini, and triggers the versioning function  
    def exportFBX_unreal(self): 
        self.unreal_el = umEl.UnMaya_Element(self.unreal_filepath)

        #initialize
        if self.unreal_shift:
            start_frame = self.shot_start
            end_frame = self.shot_end
        else:    
            start_frame = cmds.playbackOptions(ast=0, q=True)
            end_frame = cmds.playbackOptions(aet=0, q=True)
        parent_cam = self.get_shotCam(self.selected_cam)
        ##parent_cam = cmds.ls(selection=1)
        
        #create new camera
        new_cam_name = "shot_cam_" + self.shot_selection
        new_unreal_cam= cmds.camera(ar=1.85, hfa=1.748, dfg=1, n=new_cam_name)
        cmds.setAttr(str(new_unreal_cam[1]) + ".locatorScale", 15)
        
        #constrain, bake, clean up
        cmds.parentConstraint(parent_cam, new_unreal_cam[0], mo=0)
        cmds.bakeResults(new_unreal_cam[0], t=(start_frame, end_frame))
        cmds.delete(cn=1)
        
        if self.unreal_shift:
            time_shift = int(self.shot_start) * -1
            cmds.keyframe(new_unreal_cam, edit=True,relative=True,timeChange=time_shift,time=(start_frame,end_frame))

        ##mel.eval('FBXExport -f "'+path+'" -s')
        mel.eval('FBXExport -f "'+self.unreal_filepath+'" -s')

        permissions.set_permissions(self.unreal_filepath)

        #delete duplicate camera
        cmds.select(new_unreal_cam)
        cmds.delete()

        #version unreal fbx file
        self.version(self.unreal_el)



###############################################################
###                 VERSION CAM FUNCTIONS                   ### 


    def version(self, element):
        
        #Get new version number
        self.ver_num = element.get_latest_version() + 1 
        dir_name = ".v" + f"{self.ver_num:04}"
        #Make hidden directory with version number
        new_dir_path = os.path.join(self.curr_env.get_file_dir(element.filepath), dir_name) 
        os.mkdir(new_dir_path)
        #Copy FBX into the new directory and rename it
        ##new_file_path = new_dir_path + "/" + element.get_file_parent_name() + element.get_file_extension()
        new_file_path = self.get_versioned_filename(new_dir_path, element)
        shutil.copy(element.filepath, new_file_path)
        #Triggers the element file to update (must be run after the comment_gui, or else self.comment will not be set)
        self.update_element_file(element)

    def get_versioned_filename(self, new_dir_path, element):
        if element.get_file_parent_name() == "":
            return new_dir_path + "/" + self.shot_selection + element.get_file_extension()
        else:
            return new_dir_path + "/" + element.get_file_parent_name() + element.get_file_extension()

    #updates the element file with the comment
    def update_element_file(self, element):
        #Adds new publish log to list of publishes
        comment = "v" + str(self.ver_num) + ": " + self.comment_text
        element.add_publish_log(comment)
        #Set latest version
        element.set_latest_version(self.ver_num)
        #Write the .element file to disk
        element.write_element_file()
     
    #GUI: Prompts the user to imput a comment for the current export
    def comment_gui(self):
        element = umEl.UnMaya_Element(self.houdini_filepath)
        
        #Make list of past comments for the gui
        publishes = element.get_publishes_list()
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
                
    #Gets comment and triggers the exports
    def comment_results(self):
        self.comment_text = cmds.textFieldGrp('comment', q=True, text=True)
        
        if cmds.window('msCommentWindowID', exists=True):
            cmds.deleteUI('msCommentWindowID')
            
        self.trigger_exports()            
        
#Camera_Exporter()
