"""Grabs a list of all selected USD objects in Maya and replaces them with their dag object equivalent"""

import os

import ufe
from mayaUsd import lib as mayaUsdLib
import mayaUsd.lib.proxyAccessor as pa
from pxr import Sdf
import maya.cmds as mc
import maya.mel as mel
import functools, time
import logging
import pipe.pipeHandlers.environment as environment

    
def getPrimPath():
    """Gets the path of the selected primitive"""
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    primPath = Sdf.Path(selPrim)
    primPath = str(primPath)
    return primPath
    

def getPrimName():
    """Gets the name of the selected primitive"""
    primPath = getPrimPath()
    primName = str(primPath).split('/')[-2]
    return primName
        
       
def getPrimFilePath():
    """Gets the usd file path for the selected primitive """
    primName = getPrimName()
    primType = primName.split('_')[0]
    primName = primName.replace(primType + '_', '')
    primFilePath = "/groups/unfamiliar/anim_pipeline/production/assets/" + primName + "/geo/" + primType + '_' + primName + ".usd"
    print(primFilePath)
    return primFilePath
    
    
def getAssetPrimPath():
    """Gets the main primitive holding child previs and prod primitives for the selected prim"""
    primPath = getPrimPath().split('/')[1:-3]
    primPath = functools.reduce(lambda str, dir: str + dir + '/', primPath, '/')[:-1]
    return primPath
    

def getMainPrimPath():
    primPath = getPrimPath().split('/')[:4]
    primPath = functools.reduce(lambda str, dir: str + dir + '/', primPath, '/')[1:-1]
    return primPath
    
        
def hidePrim():
    """Hides the selected primitive"""
    mel.eval('toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`')
    

def importDAG():
    """Imports the DAG object for the selected primitive"""
    mc.file(getPrimFilePath(), i = True, type = "USD Import")
    

def deleteParent(object):
    """Deletes the parent of the provided object"""
    parents = mc.listRelatives(object, allParents = True)
    if parents != None:
        deleteParent(parents[0])
    if mc.objExists(object):
        mc.delete(object)
        

def logMessage(logName, message):
    """Logs a message to the Maya logger"""
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
    
    
def replacePrim():
    """Replaces a primitive with its dag object equivalent. 
    Will import the dag object, but not place it in the right world space"""
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
    # melCommand = 'mayaUsdDuplicate "' + selDag + ',' + mainPrimPath + '" "|world";'
    melCommand = f"mayaUsdDuplicate \"{selDag},{mainPrimPath}\" \"|world\";"
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


def replacePrimWithReference():
    """Replaces a primitive with its dag object equivalent through a reference for convenience when refreshing. 
    Will import the dag object, but not place it in the right world space"""
    #get prim info
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    primPath = getPrimPath()
    primName = getPrimName()
    assetName = getAssetPrimPath().split('/')[-1]
    mainPrimPath = getMainPrimPath()

    #hide prim
    hidePrim()

    """
    Here, we could use maya.standalone to open a new maya session and import the model, then reference it back into the current session
    It might be really slow, will have to test 

    Otherwise, we can save the current scene, open a new one, import the model, then reference it back into the original scene
    """

    # Save the current scene 
    originalScene = mc.file(s=True)  # If this fails, the script shouldn't continue 

    # Open a new scene
    mc.file(new=True, force=True)

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

    # Save the new scene
    newScenePath = os.path.join(os.path.dirname(originalScene), primName + '_PROD.ma')
    newScene = mc.file(newScenePath, s=True, rename=)



def refreshPrim():
    """Refreshes the referenced primitive object from the USD file"""
    pass


class mayaRun:
    def run(self):
        replacePrim()
    
    def runWithReference(self):
        replacePrimWithReference()

    def refresh(self):
        refreshPrim()