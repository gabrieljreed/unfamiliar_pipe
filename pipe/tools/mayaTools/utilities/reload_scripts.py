import importlib as il
from pipe.tools.mayaTools import *
from pipe.tools.mayaTools.utilities import utils as maya_utils
from pipe.tools.mayaTools.utilities import reload_scripts
##from pipe.pipeHandlers import select_from_list as sfl


class ReloadScripts:

    def go(self):
        il.reload(reload_scripts)
        il.reload(maya_utils)
        ##il.reload(sfl)
