from pipe.pipeHandlers.environment import Environment as env
import pipe.pipeHandlers.permissions as permissions
import json
import os
import functools
import time


class Element:
    """This class is an io utility for the .element files that keep track of version control, shot accessibility, etc.
    It is an abstract class describing elements that make up an asset or shot body."""

    PUBLISHES = "publishes"
    PIPELINE_FILENAME = ".element"
    NAME = "name"
    PARENT = "parent"
    LATEST_VERSION = "latest_version"
    APP_EXT = "app_ext"
    ASSIGNED_USER = "assigned_user"

    def __init__(self, filepath):
        """Requires filepath of file of which we want to access the respective .element file"""
        self.filepath = filepath
        self.datadict = None
        self.elementpath = self.get_element_path()
        self.retrieve_element_file()

    def get_element_path(self):
        """Creates the .element file path"""
        self.element_path = env().get_file_dir(self.filepath) + "/.element"

    def create_new_dict(self):
        """Creates a datadict for the given file"""
        datadict = {}
        datadict[Element.PUBLISHES] = []
        datadict[Element.NAME] = env().get_file_name_extension(filepath=self.filepath)[0].split('_')[-1]
        parent_name = env().get_file_name_extension(self.filepath)[0].split('_')[:-1]
        parent_name = functools.reduce(lambda str, name: str + name + '_', parent_name, '')[:-1]
        datadict[Element.PARENT] = parent_name
        datadict[Element.LATEST_VERSION] = -1
        datadict[Element.APP_EXT] = env().get_file_name_extension(self.filepath)[1]
        datadict[Element.ASSIGNED_USER] = ""
        self.datadict = datadict

    def write_element_file(self):
        """Writes the datadict to the respective .element file"""
        json_object = json.dumps(self.datadict, indent=4)
        file = open(self.element_path, 'w')
        file.write(json_object)
        file.close()
        permissions.set_permissions(self.element_path)

    def retrieve_element_file(self):
        """Checks if a .element file exists in the pipe. If it does, it opens it and inputs the data into the datadict.
        If it doesn't exist, a new datadict and .element file are created."""
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

    def is_assigned(self):
        """Checks to see if the shot is assigned or not"""
        if self.datadict[Element.ASSIGNED_USER] == '':
            return False
        else:
            return True

    def get_assigned_user(self):
        return self.datadict[Element.ASSIGNED_USER]

    def assign_user(self, user):
        """Assigns the specified user to the datadict"""
        self.datadict[Element.ASSIGNED_USER] = user

    def get_latest_version(self):
        return self.datadict[Element.LATEST_VERSION]

    def set_latest_version(self, version_number):
        self.datadict[Element.LATEST_VERSION] = version_number

    def get_file_parent_name(self):
        """Returns parent name of file
        ex: file 'a004_main.hipnc' has a parent name 'a004'"""
        file_parent_name = self.datadict[Element.PARENT]
        return file_parent_name

    def get_file_ext(self):
        """Returns file extension"""
        ext = self.datadict[Element.APP_EXT]
        return ext

    def add_publish_log(self, message):
        log = []
        # Add username to log
        log.append(env().get_username())
        # Add timestamp to log
        log.append(time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime()))
        # Add message to log
        log.append(message)
        # Add file path to log
        log.append(self.filepath)
        # Add log to the datadict
        self.datadict[Element.PUBLISHES].append(log)

    def get_publishes_list(self):
        return self.datadict[Element.PUBLISHES]
