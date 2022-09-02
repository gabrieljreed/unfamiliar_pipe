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
    
    def addMenuItem(self, parent, label, command=defaultNullFunc, icon=""):
        """Adds a menu item to the specified parent menu"""
        if icon != "":
            icon = self.iconPath + icon
        return mc.menuItem(label=label, command=command, image=icon, parent=parent)

    def addSubMenu(self, parent, label, icon=None):
        """Adds a sub menu to the specified parent menu"""
        if icon != "":
            icon = self.iconPath + icon
        return mc.menuItem(label=label, subMenu=True, image=icon, parent=parent)

    def addSeparator(self,):
        """Adds a separator to the shelf"""
        mm.eval("addShelfSeparator()")
    
    def cleanOldShelf(self):
        """Checks if old shelf exists and empties it if it does, or create it if it does not"""
        if mc.shelfLayout(self.name, ex=True):
            if mc.shelfLayout(self.name, q=True, ca=True):
                for each in mc.shelfLayout(self.name, q=True, ca=True):
                    mc.deleteUI(each)
        else:
            mc.shelfLayout(self.name, p=getTopLevelShelf())
