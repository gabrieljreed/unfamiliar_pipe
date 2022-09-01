import maya.cmds as mc
import maya.mel as mm
import os 
import abc

def defaultNullFunc(*args):
    pass


def getTopLevelShelf():
    return mm.eval("$tmpVar=$gShelfTopLevel")


class ShelfBase(object):
    """A simple class to build shelves in Maya. By default it creates an empty shelf called 'customShelf'"""

    def __init__(self, name="customShelf", iconPath=""):
        __metaclass__ = abc.ABCMeta

        self.name = name
        self.iconPath = iconPath

        self.labelBackground = (0, 0, 0, 0)
        self.labelColor = (0.9, 0.9, 0.9)

        self.cleanOldShelf()
        mc.setParent(self.name)
        self.build()
    
    @abc.abstractmethod
    def build(self):
        """This method must be overridden in the child class"""
        raise NotImplementedError("Subclass must implement abstract method")
    
    def addButton(self, desc, icon="", command=defaultNullFunc, doubleCommand=defaultNullFunc):
        """Adds a shelf button with the specified label, command, double click command, and image"""
        mc.setParent(self.name)
        if icon != "":
            icon = self.iconPath + icon
        
        return mc.shelfButton(width=37, height=37, image=icon, l=desc, ann=desc, command=command, dcc=doubleCommand, olb=self.labelBackground, olc=self.labelColor, noDefaultPopup=True)
