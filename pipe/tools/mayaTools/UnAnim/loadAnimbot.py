import os

import maya.mel as mel
import maya.cmds as mc


def loadAnimbot():
    plugDir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "tools", "external", "AnimSchoolPicker"))
    curVersion = "maya{}".format(mc.about(v=True))

    plugPath = os.path.normpath("/usr/autodesk/ApplicationPlugins/animBot/plug-ins/animBot.py")

    mel.eval('loadPlugin -qt "' + plugPath + '"')

class mayaRun:
    def run(self):
        loadAnimbot()
