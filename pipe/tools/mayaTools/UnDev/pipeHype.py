import maya.cmds as mc


def pipeHype():
    mc.scriptEditorInfo(clearHistory=True)
    mc.evalDeferred("print('PIPE HYPE')")


class mayaRun:
    def run(self):
        pipeHype()
