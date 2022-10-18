import os
import functools


class UnMaya_Environment:
    """This class mimics the environment.py file that is used for Houdini (just simplified and for what is needed and
    adjusted filepaths)"""

    # Set directory filepaths
    # SHOT_DIR = '/groups/unfamiliar/animation/Pipeline_Shots'
    SHOT_DIR = '/groups/unfamiliar/anim_pipeline/production/anim_shots'
    ICON_DIR = '/groups/unfamiliar/anim_pipeline/icons'

    def __init__(self):
        """Sets the project directory as defined in the MEDIA_PROJECT_DIR environment variable"""
        self.project_dir = os.getenv('MEDIA_PROJECT_DIR')

    def get_shot_dir(self):
        """Gets the directory for all shot directories"""
        return self.SHOT_DIR
        # shot_dir = self.project_dir + self.SHOT_DIR
        # return shot_dir

    def get_shot_list(self):
        """Gets a list of all shot names"""
        shot_list = os.listdir(self.get_shot_dir())
        return shot_list

    def get_shot_list_undef(self, shot_dir):
        shot_list = os.listdir(shot_dir)
        return shot_list

    def get_mb_dir(self, shot_name):
        """Gets the maya mb directory from a shot name (also currently hardcoded for an .mb, may need to change this
         later if an .ma is needed isntead)"""
        mb_dir = self.get_shot_dir() + '/' + shot_name + '/' + shot_name + '_main.mb'
        return mb_dir

    def get_file_dir(self, filepath):
        """Gets the directory holding the file specified in the filepath argument"""
        file_dir = filepath.split('/')[:-1]
        if file_dir[0] == '':
            file_dir.pop(0)
        file_dir = functools.reduce(lambda str, dir: str + dir + '/', file_dir, '/')[:-1]
        return file_dir

    def get_file_name_extension(self, filepath):
        """Gets both the name of the file and its extention in a touple for
        the file specified in the filepath argument"""
        temp_file = filepath.split('/')[-1]
        file_name, file_extension = os.path.splitext(temp_file)
        return [file_name, file_extension]

    def get_username(self):
        """Gets the current user username"""
        return os.getenv('HOME').split('/')[-1]
