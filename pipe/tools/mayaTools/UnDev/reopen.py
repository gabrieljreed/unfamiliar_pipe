"""Reopens the current file without saving"""

import maya.cmds as mc


def reopen():
    """Reopens the current file without saving"""
    currentFile = mc.file(q=True, sn=True)
    mc.file(currentFile, f=True, o=True)


class mayaRun():
    def run(self):
        reopen()
