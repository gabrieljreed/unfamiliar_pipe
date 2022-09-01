import ufe
from mayaUsd import lib as mayaUsdLib
import mayaUsd.lib.proxyAccessor as pa
from pxr import Sdf
import maya.cmds as mc
import maya.mel as mel
import functools, time
import logging
import pipe.pipeHandlers.environment as environment

    
#Gets the path of the selected primitive
def getPrimPath():
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    primPath = Sdf.Path(selPrim)
    primPath = str(primPath)
    return primPath
    

#gets the name of the selected primitive
def getPrimName():
    primPath = getPrimPath()
    primName = str(primPath).split('/')[-2]
    return primName
        
       
#gets the usd file path for the selected primitive 
def getPrimFilePath():
    primName = getPrimName()
    primType = primName.split('_')[0]
    primName = primName.replace(primType + '_', '')
    primFilePath = "/groups/unfamiliar/anim_pipeline/production/assets/" + primName + "/geo/" + primType + '_' + primName + ".usd"
    print(primFilePath)
    return primFilePath
    
    
#gets the main primitive holding child previs and prod primitives for the selected prim
def getAssetPrimPath():
    primPath = getPrimPath().split('/')[1:-3]
    primPath = functools.reduce(lambda str, dir: str + dir + '/', primPath, '/')[:-1]
    return primPath
    

def getMainPrimPath():
    primPath = getPrimPath().split('/')[:4]
    primPath = functools.reduce(lambda str, dir: str + dir + '/', primPath, '/')[1:-1]
    return primPath
    
        
#hides the selected primitive
def hidePrim():
    mel.eval('toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`')
    

#imports the DAG object for the selected primitive
def importDAG():
    mc.file(getPrimFilePath(), i = True, type = "USD Import")
    

def deleteParent(object):
    parents = mc.listRelatives(object, allParents = True)
    if parents != None:
        deleteParent(parents[0])
    if mc.objExists(object):
        mc.delete(object)
        
def logMessage(logName, message):
    logger = logging.getLogger(logName)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # prevent logging from bubbling up to maya's logger
    logger.propagate=0
    # 'application' code
    logger.info(message)
    
    
#replaces a primitive with its dag object equivalent
#will import the dag object, but not place it in the right world space
def replacePrim():
    #get prim info
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    primPath = getPrimPath()
    primName = getPrimName()
    assetName = getAssetPrimPath().split('/')[-1]
    mainPrimPath = getMainPrimPath()
    #hide prim
    hidePrim()
    #duplicate to maya
    melCommand = 'mayaUsdDuplicate "' + selDag + ',' + mainPrimPath + '" "|world";'
    mel.eval(melCommand)
    #Get all parent info
    parents = mc.listRelatives(assetName, allParents = True)
    #Parent asset to world and delete all old parents
    if parents != None:
        mc.parent(assetName, world=True)
        deleteParent(parents[0])
    #delete production asset
    mc.delete("previs_" + assetName)
    #make asset visible
    mc.select('mesh_0')
    mc.showHidden('mesh_0')
    mc.rename(primName + '_PROD')
    logMessage('Production Model Import', 'Model imported successfully lets goooooo')


class mayaRun:
    def run(self):
        replacePrim()