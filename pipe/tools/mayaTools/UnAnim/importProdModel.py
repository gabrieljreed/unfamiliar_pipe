"""Grabs a list of all selected USD objects in Maya and replaces them with their dag object equivalent"""

import os
import json

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
    melCommand = 'mayaUsdDuplicate "' + selDag + ',' + mainPrimPath + '" "|world";'
    # melCommand = f"mayaUsdDuplicate \"{selDag},{mainPrimPath}\" \"|world\";"
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
    # get prim info
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    primPath = getPrimPath()
    primName = getPrimName()
    assetName = getAssetPrimPath().split('/')[-1]
    mainPrimPath = getMainPrimPath()

    # hide prim
    hidePrim()

    # duplicate to maya
    melCommand = 'mayaUsdDuplicate "' + selDag + ',' + mainPrimPath + '" "|world";'
    mel.eval(melCommand)

    # Get all parent info
    parents = mc.listRelatives(assetName, allParents=True)
    # Parent asset to world and delete all old parents

    if parents is not None:
        mc.parent(assetName, world=True)
        deleteParent(parents[0])

    # delete production asset
    mc.delete("previs_" + assetName)

    # make asset visible
    mc.select('mesh_0')  # FIXME: This breaks sometimes
    mc.showHidden('mesh_0')
    mc.rename(primName + '_PROD')
    logMessage('Production Model Import', 'Model imported successfully lets goooooo')

    # Get the current scene to do cool stuff
    originalScene = mc.file(query=True, sceneName=True)

    # Create reference folder
    refFolder = os.path.join(os.path.dirname(originalScene), "references")
    if not os.path.exists(refFolder):
        os.mkdir(refFolder)

    # Save the new scene
    fbxExportPath = os.path.join(os.path.dirname(originalScene), "references", assetName + '_REF.fbx')
    refFilePath = mc.file(fbxExportPath, exportSelected=True, type="FBX export", force=True)

    # Write assetInfo out to a file so it can be reloaded later
    referencesFile = None
    for file in os.listdir(refFolder):
        if file.endswith("references.txt"):
            referencesFile = os.path.join(refFolder, file)
            break

    # If the references file is not found, create it
    if referencesFile is None:
        referencesFile = os.path.join(refFolder, "references.json")
        with open(referencesFile, 'w') as f:
            f.write('{"referenceList": []}')

    assetInfo = {"assetName": assetName, "mainPrimPath": mainPrimPath, "primName": primName, "selDag": selDag}

    with open(referencesFile, 'r') as f:
        references = json.load(f)
        references["referenceList"].append(assetInfo)

    with open(referencesFile, 'w') as f:
        json.dump(references, f)

    # Delete the newly created asset and instead reference it in
    mc.delete(assetName)
    mc.file(refFilePath, reference=True, type="FBX", namespace="REF")

    # TODO: Make sure top level thing is the same as asset name for alembic exporting


def refreshAllPrims():
    """Refreshes all referenced prims in the scene"""
    # Get the current scene to do cool stuff
    originalScene = mc.file(query=True, sceneName=True)

    # Look for the references file
    refFolder = os.path.join(os.path.dirname(originalScene), "references")
    if not os.path.isdir(refFolder):
        mc.warning("No references folder found")
        return

    referencesFile = None
    for file in os.listdir(refFolder):
        if file.endswith("references.json"):
            referencesFile = os.path.join(refFolder, file)
            break

    if referencesFile is None:
        mc.warning("No references file found")
        return

    with open(referencesFile, 'r') as f:
        references = json.load(f)
        for reference in references["referenceList"]:
            # Check if the asset name exists in the maya scene 
            if mc.objExists(reference["assetName"]):
                mc.error("Asset already exists in scene")
                continue
            # Duplicate the prim
            melCommand = 'mayaUsdDuplicate "' + reference["selDag"] + ',' + reference["mainPrimPath"] + '" "|world";'
            mel.eval(melCommand)

            # Get all parent info
            parents = mc.listRelatives(reference["assetName"], allParents=True)
            # Parent asset to world and delete all old parents

            if parents is not None:
                mc.parent(reference["assetName"], world=True)
                deleteParent(parents[0])

            # delete production asset
            mc.delete("previs_" + reference["assetName"])

            # make asset visible
            mc.select('mesh_0')
            mc.showHidden('mesh_0')
            mc.rename(reference["primName"] + '_PROD')
            logMessage('Production Model Import', 'Model imported successfully lets goooooo')

            fbxExportPath = os.path.join(os.path.dirname(originalScene), "references", reference["assetName"] + '_REF.fbx')
            refFilePath = mc.file(fbxExportPath, exportSelected=True, type="FBX export", force=True)
            print("Re-exported reference FBX to: " + refFilePath)
            # Delete the asset
            mc.delete(reference["assetName"])

    references = mc.ls(type="reference")
    for ref in references:
        try:
            refPath = mc.referenceQuery(ref, filename=True)
        except Exception as e:
            print("ERROR LOADING {}: {}".format(ref, e))
            continue
        if refPath.endswith(".fbx"):
            mc.file(refPath, loadReference=True, loadReferenceDepth="all")
            print("RELOADED REFERENCE: " + refPath)


def refreshPrim():
    """Refreshes the referenced primitive object from the USD file"""
    print("Error, this function is not yet implemented")


class mayaRun:
    def run(self):
        replacePrim()

    def runWithReference(self):
        replacePrimWithReference()

    def refresh(self):
        refreshAllPrims()
