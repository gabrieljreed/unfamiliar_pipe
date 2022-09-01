from pipe.pipeHandlers.environment import Environment as env
import json
import os, functools, time

#This class is an io utility for the .element files that keep track of version
#control, shot accessibility, etc.
class Element:
    
    #Abstract class describing elements that make up an asset or shot body.
    PUBLISHES = "publishes"
    PIPELINE_FILENAME = ".element"
    NAME = "name"
    PARENT = "parent"
    LATEST_VERSION = "latest_version"
    APP_EXT = "app_ext"
    ASSIGNED_USER = "assigned_user"

    #Requires filepath of file of which we want to access the respective .element file
    def __init__(self, filepath):
        self.filepath = filepath
        self.datadict = None
        self.elementpath = self.get_element_path()
        self.retrieve_element_file()


    #Creates the .element file path
    def get_element_path(self):
        self.element_path = env().get_file_dir(self.filepath) + "/.element"


    #Creates a datadict for the given file
    def create_new_dict(self):
        datadict = {}
        datadict[Element.PUBLISHES] = []
        datadict[Element.NAME] = env().get_file_name_extension(filepath = self.filepath)[0].split('_')[-1]
        parent_name = env().get_file_name_extension(self.filepath)[0].split('_')[:-1]
        parent_name = functools.reduce(lambda str, name: str + name + '_', parent_name, '')[:-1]
        datadict[Element.PARENT] = parent_name
        datadict[Element.LATEST_VERSION] = -1
        datadict[Element.APP_EXT] = env().get_file_name_extension(self.filepath)[1]
        datadict[Element.ASSIGNED_USER] = ""
        self.datadict = datadict


    #Writes the datadict to the respective .element file
    def write_element_file(self):
        json_object = json.dumps(self.datadict, indent = 4)
        file = open(self.element_path, 'w')
        file.write(json_object)
        file.close()


    #Checks if a .element file exists in the pipe. If it does, it opens it and
    #inputs the data into the datadict. If it doesn't exist, a new datadict and
    #.element file are created.
    def retrieve_element_file(self):
        if os.path.isfile(self.element_path):
            with open(self.element_path) as json_file:
                data = json.load(json_file)
                datadict = {}
                datadict[Element.PUBLISHES] = data['publishes']
                datadict[Element.NAME] = data['name']
                datadict[Element.PARENT] = data['parent']
                datadict[Element.LATEST_VERSION] = data['latest_version']
                datadict[Element.APP_EXT] = data['app_ext']
                datadict[Element.ASSIGNED_USER] = data['assigned_user']
                self.datadict = datadict
        else:
            print("creating .element file")
            self.create_new_dict()
            self.write_element_file()


    #Checks to see if the shot is assigned or not
    def is_assigned(self):
        if self.datadict[Element.ASSIGNED_USER] == '':
            return False
        else:
            return True


    def get_assigned_user(self):
        return self.datadict[Element.ASSIGNED_USER]


    #Assigns the specified user to the datadict
    def assign_user(self, user):
        self.datadict[Element.ASSIGNED_USER] = user

    
    def get_latest_version(self):
        return self.datadict[Element.LATEST_VERSION]

    
    def set_latest_version(self, version_number):
        self.datadict[Element.LATEST_VERSION] = version_number

    #Returns parent name of file
    #ex: file 'a004_main.hipnc' has a parent name 'a004'
    def get_file_parent_name(self):
        file_parent_name = self.datadict[Element.PARENT]
        return file_parent_name


    #Returns file extension
    def get_file_ext(self):
        ext = self.datadict[Element.APP_EXT]
        return ext


    def add_publish_log(self, message):
        log = []
        #Add username to log
        log.append(env().get_username())
        #Add timestamp to log
        log.append(time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime()))
        #Add message to log
        log.append(message)
        #Add file path to log
        log.append(self.filepath)
        #Add log to the datadict
        self.datadict[Element.PUBLISHES].append(log)


    def get_publishes_list(self):
        return self.datadict[Element.PUBLISHES]
