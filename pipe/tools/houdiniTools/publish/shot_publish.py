import hou
import pipe.pipeHandlers.quick_dialogs as qd
from pipe.pipeHandlers.environment import Environment as env
import pipe.pipeHandlers.gui as gui
from pipe.pipeHandlers.element import Element
import os, shutil

#This class publishes the shot back to the pipe. This includes version control.
class ShotPublish:

    def __init__(self):
        #Get shot list
        self.shot_list = env().get_shot_list()


    #Starts the gui for publishing shots
    def publish(self):
        #Intilize gui with the shot list
        self.item_gui = gui.SelectFromList(l=self.shot_list, parent=hou.ui.mainQtWindow(), title="Select a shot to publish")
        #Send results from gui to the results method
        self.item_gui.submitted.connect(self.results)


    #Is called after the user interacts with the gui
    def results(self, value):
        print("Selected shot: " + value[0])
        #Get the hip directory
        hip_dir = env().get_hip_dir(value[0])
        #Access the respective .element file
        self.el = Element(hip_dir)
        #Get comment from user
        self.get_comment()
        

    #Gui for submitting comments
    def get_comment(self):
        #Make list of past comments for the gui
        publishes = self.el.get_publishes_list()
        if len(publishes) > 10:
            publishes = publishes[-10:]
        publishes_string_list = ""
        for publish in publishes:
            label = publish[0] + " " + publish[1] + " " + publish[2] + "\n"
            publishes_string_list += label

        #Make gui
        self.input = qd.HoudiniInput(parent=hou.qt.mainWindow(), title="Comment ", info=publishes_string_list)
        self.input.submitted.connect(self.comment_results)


    #Result of comment gui. Gets comment value, versions the file and updates the .element file
    def comment_results(self, value):
        self.comment = ''.join(value)
        self.version_file()
        self.update_element_file()
        hou.ui.displayMessage('Successfully published shot.')


    #Saves and versions the hip file
    def version_file(self):
        #Save current hip file in main directory
        hou.hipFile.save()
        #Get new version number
        self.ver_num = self.el.get_latest_version() + 1
        dir_name = ".v" + f"{self.ver_num:04}"
        #make hidden directory with version number
        new_dir_path = os.path.join(env().get_file_dir(self.el.filepath), dir_name)
        os.mkdir(new_dir_path)
        #Copy current hip file into new directory and rename it.
        new_file_path = new_dir_path + '/' + self.el.get_file_parent_name() + self.el.get_file_ext()
        shutil.copy(self.el.filepath, new_file_path)
        

    def update_element_file(self):
        #Adds new publish log to list of publishes
        self.el.add_publish_log(self.comment)
        #Set latest version
        self.el.set_latest_version(self.ver_num)
        #Remove assigned user
        self.el.assign_user('')
        #Write the .element file to disk
        self.el.write_element_file()
