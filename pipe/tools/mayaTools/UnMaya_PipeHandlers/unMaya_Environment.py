import maya.cmds as cmds
import json
import os, shutil, functools, time


# This class mimics the environment.py file that is used for Houdini (just simplified and for what is needed and adjusted filepaths)
class UnMaya_Environment:
    
    #Set directory filepaths
    ##SHOT_DIR = '/groups/unfamiliar/animation/Pipeline_Shots'
    SHOT_DIR = '/groups/unfamiliar/anim_pipeline/production/anim_shots'
    ICON_DIR = '/groups/unfamiliar/anim_pipeline/icons'
    
    #Sets the project directory as defined in the MEDIA_PROJECT_DIR environment variable
    def __init__(self):
        self.project_dir = os.getenv('MEDIA_PROJECT_DIR')
    
    #Gets the directory for all shot directories    
    def get_shot_dir(self):
        return self.SHOT_DIR
        ##shot_dir = self.project_dir + self.SHOT_DIR
        ##return shot_dir
    
    #Gets a list of all shot names    
    def get_shot_list(self):
        shot_list = os.listdir(self.get_shot_dir())
        return shot_list
    
    def get_shot_list_undef(self, shot_dir):
        shot_list = os.listdir(shot_dir)
        return shot_list
    
    #Gets the maya mb directory from a shot name (also currently hardcoded for an .mb, may need to change this later if an .ma is needed isntead)    
    def get_mb_dir(self, shot_name):
        mb_dir = self.get_shot_dir() + '/' + shot_name + '/' + shot_name + '_main.mb'
        return mb_dir
        
    #gets the directory holding the file specified in the filepath argument    
    def get_file_dir(self, filepath):
        file_dir = filepath.split('/')[:-1]
        if file_dir[0] == '':
            file_dir.pop(0)
        file_dir = functools.reduce(lambda str, dir: str + dir + '/', file_dir, '/')[:-1]
        return file_dir
    
    #Gets both the name of the file and its extention in a touple for 
    #the file specified in the filepath argument    
    def get_file_name_extension(self, filepath):
        temp_file = filepath.split('/')[-1]
        file_name, file_extension = os.path.splitext(temp_file)
        return [file_name, file_extension]
    
    #Gets the current user username    
    def get_username(self):
        return os.getenv('HOME').split('/')[-1]
        

