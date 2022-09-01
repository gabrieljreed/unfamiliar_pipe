import os, functools

#This class allows easy access to various environment information
class Environment:

    PROJECT_ENV = 'MEDIA_PROJECT_DIR'
    ASSET_DIR = '/production/assets'
    SHOT_DIR = '/production/shots'
    ICON_DIR = '/icons'

    #Sets the project directory as defined in the MEDIA_PROJECT_DIR envrionment variable
    def __init__(self):
        self.project_dir = os.getenv('MEDIA_PROJECT_DIR')


    #Gets the directory for all assets
    def get_asset_dir(self):
        asset_dir = self.project_dir + self.ASSET_DIR
        return asset_dir


    #Gets a list of all assets in the asset directory
    def get_asset_list(self):
        asset_list = os.listdir(self.get_asset_dir())
        return asset_list


    #Gets the directory for all shot directories
    def get_shot_dir(self):
        shot_dir = self.project_dir + self.SHOT_DIR
        return shot_dir


    #Gets a list of all shot names
    def get_shot_list(self):
        shot_list = os.listdir(self.get_shot_dir())
        return shot_list


    #Gets the icon directory (needed for gui.py but I haven't looked in to why that is)
    def get_icon_dir(self):
        icon_dir = self.project_dir + self.ICON_DIR
        return icon_dir


    #Gets the directory holding the file specified in the filepath argument
    def get_file_dir(self, filepath):
        file_dir = filepath.split('/')[:-1]
        file_dir = functools.reduce(lambda str, dir: str + dir + '/', file_dir, '/')[:-1]
        return file_dir


    #Gets both the name of the file and its extention in a touple for 
    #the file specified in the filepath argument
    def get_file_name_extension(self, filepath):
        file = filepath.split('/')[-1]
        file_name, file_extension = os.path.splitext(file)
        return [file_name, file_extension]


    #Gets the current users username
    def get_username(self):
        return os.getenv('HOME').split('/')[-1]

    
    #Gets the hip directory from a shot name
    def get_hip_dir(self, shot_name):
        #This could be more robust and is a little too hard coded rn
        hip_dir = self.get_shot_dir() + '/' + shot_name + '/' + shot_name + '_main.hipnc'
        return hip_dir
