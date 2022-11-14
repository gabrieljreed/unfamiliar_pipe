import os
import functools


class Environment:
    """ This class allows easy access to various environment information """

    PROJECT_ENV = 'MEDIA_PROJECT_DIR'
    ASSET_DIR = '/production/assets'
    SHOT_DIR = '/production/shots'
    ICON_DIR = '/icons'
    RIG_DIR = '/production/rigs'

    def __init__(self):
        """Sets the project directory as defined in the MEDIA_PROJECT_DIR envrionment variable"""
        self.project_dir = os.getenv('MEDIA_PROJECT_DIR')

    def get_asset_dir(self):
        """Gets the directory for all assets"""
        asset_dir = self.project_dir + self.ASSET_DIR
        return asset_dir

    def get_asset_list(self):
        """Gets a list of all assets in the asset directory"""
        asset_list = os.listdir(self.get_asset_dir())
        return asset_list

    def get_shot_dir(self):
        """Gets the directory for all shot directories"""
        shot_dir = self.project_dir + self.SHOT_DIR
        return shot_dir

    def get_shot_list(self):
        """Gets a list of all shot names"""
        shot_list = os.listdir(self.get_shot_dir())
        return shot_list

    def get_icon_dir(self):
        """Gets the icon directory (needed for gui.py but I haven't looked in to why that is)"""
        icon_dir = self.project_dir + self.ICON_DIR
        return icon_dir

    def get_file_dir(self, filepath):
        """Gets the directory holding the file specified in the filepath argument"""
        file_dir = filepath.split('/')[:-1]
        file_dir = functools.reduce(lambda str, dir: str + dir + '/', file_dir, '/')[:-1]
        return file_dir

    def get_file_name_extension(self, filepath):
        """Gets both the name of the file and its extention in a tuple for the file specified in the filepath
         argument"""
        file = filepath.split('/')[-1]
        file_name, file_extension = os.path.splitext(file)
        return [file_name, file_extension]

    def get_username(self):
        """Gets the current users username"""
        return os.getenv('HOME').split('/')[-1]

    def get_hip_dir(self, shot_name):
        """Gets the hip directory from a shot name"""
        # TODO: This could be more robust and is a little too hard coded rn
        hip_dir = self.get_shot_dir() + '/' + shot_name + '/' + shot_name + '_main.hipnc'
        return hip_dir

    def get_nuke_dir(self, shot_name):
        """Gets the nuke directory from a shot name"""
        nuke_dir = os.path.join(self.get_shot_dir(), shot_name, "nuke", shot_name + '_main.nk')
        return nuke_dir

    def get_rig_dir(self):
        """Gets the rig directory"""
        rig_dir = self.project_dir + self.RIG_DIR
        return rig_dir

    def get_rig_prop_dir(self):
        """Gets the rig prop directory"""
        rig_prop_dir = self.get_rig_dir() + '/props'
        return rig_prop_dir
