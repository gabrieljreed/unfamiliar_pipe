from mayaUsd import lib as mayaUsdLib
import ufe
from pxr import Sdf
import mayaUsd.lib.proxyAccessor as pa
import maya.cmds as mc
import logging
import pipe.pipeHandlers.environment as environment


def getPrimPathFromDAG(object):
    #get correct object name
    object = object.replace('_ANIM', '')
    env = environment.Environment()
    curDir = env.get_file_dir(mc.file(q=True, sn=True))[1:]
    f = curDir + '/.prims.txt'
    f = open(f, "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.replace("\n", "")
        objectName = line.split('/')[-2]
        if (objectName == object):
            return line
    return "no animatible prim"


def getDAGtransform(object, type):
    if (type == "xformOp:rotateXYZ"):
        rot = [mc.getAttr(object + ".rotateX"), mc.getAttr(object + ".rotateY"), mc.getAttr(object + ".rotateZ")]
        return rot
    elif (type == "xformOp:translate"):
        tran = [mc.getAttr(object + ".translateX"), mc.getAttr(object + ".translateY"), mc.getAttr(object + ".translateZ")]
        return tran
    elif (type == "xformOp:scale"):
        sc = [mc.getAttr(object + ".scaleX"), mc.getAttr(object + ".scaleY"), mc.getAttr(object + ".scaleZ")]
        return sc
    else:
        return "error"


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


def bakeAnim():
    #select animated objects
    animatedObjects = mc.ls(sl = True)
    for object in animatedObjects: 
        #get prim path
        primPath = getPrimPathFromDAG(object)
        #print(object)
        #print(primPath)
        mc.select(primPath)
        #get prim info for keyframing
        ufeObject = pa.getUfeSelection()
        selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
        print(selPrim)
        stage = mayaUsdLib.GetPrim(selDag).GetStage()
        primPath = Sdf.Path(selPrim)
        prim = stage.GetPrimAtPath(primPath)
        pa.createXformOps(ufeObject)
        #for loop for frame range
        for i in range(1, int(mc.playbackOptions(q = True, max = True)) + 1):
            mc.currentTime(i, edit = True)
            #for loop for transforms
            for usdAttr in ["xformOp:rotateXYZ", "xformOp:translate", "xformOp:scale"]:
                xformop = prim.GetAttribute(usdAttr)
                pos = getDAGtransform(object, usdAttr)
                #Add a time sample to the xformOp at frame i
                xformop.Set(time=i, value=tuple(pos))
        logMessage('USD ANIM EXPORT', 'Exported animation for ' + object)
    logMessage('USD ANIM EXPORT', 'All animation exported lets goooooo')
        

class mayaRun:
    def run(self):     
        bakeAnim()

