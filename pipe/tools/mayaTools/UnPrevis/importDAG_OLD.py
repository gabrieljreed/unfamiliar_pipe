import ufe
from mayaUsd import lib as mayaUsdLib
import mayaUsd.lib.proxyAccessor as pa
from pxr import Sdf
import maya.cmds as mc
import maya.mel as mel
import functools, time
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
def getMainPrimPath():
    primPath = getPrimPath().split('/')[1:-3]
    primPath = functools.reduce(lambda str, dir: str + dir + '/', primPath, '/')[:-1]
    return primPath
    
        
#hides the selected primitive
def hidePrim():
    mel.eval('toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`')
    

#imports the DAG object for the selected primitive
def importDAG():
    mc.file(getPrimFilePath(), i = True, type = "USD Import")


'''
#gets the position of the selected primitve from the main primitive it is child to
#UPDATE: I couldn't get this one working. Animators will have to move the objects by hand
#    It would be hard to make this work, because you would have to account for all
#    the transformations in the hiearchy to get the exact same global location
def getPrimPos():
    selPrimPath = getPrimPath()
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    mainPrimPath = getMainPrimPath()
    mc.select(selDag + ',' + mainPrimPath)
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    stage = mayaUsdLib.GetPrim(selDag).GetStage()
    primPath = Sdf.Path(selPrim)
    prim = stage.GetPrimAtPath(primPath)
    pa.createXformOps(ufeObject)
    xformop_translate = prim.GetAttribute("xformOp:translate")
    xformop_rotate = prim.GetAttribute("xformOp:rotateXYZ")
    tran = xformop_translate.Get()
    rot = xformop_rotate.Get()
    print(tran)
    print(rot)
    return tran, rot
'''
    
#replaces a primitive with its dag object equivalent
#will import the dag object, but not place it in the right world space
def replacePrim():
    #get prim info
    ufeObject = pa.getUfeSelection()
    selDag, selPrim = pa.getDagAndPrimFromUfe(ufeObject)
    primPath = getPrimPath()
    primName = getPrimName()
    #primPos = getPrimPos()
    DAGname = 'mesh_0'
    #hide prim
    hidePrim()
    #import dag
    importDAG()
    #rename dag
    mc.select(DAGname)
    mc.rename(primName)
    #rename dag group
    dag = mc.ls(sl = True)[0]
    parentGroup = mc.listRelatives(ap = True)[0]
    mc.rename('MOVE_GRP_TO_OG_LOCATION')
    #put prim transforms on DAG - BROKEN RN DOESNT WORK
    #mc.move(primPos[0][0], primPos[0][1], primPos[0][2])
    #mc.rotate(primPos[1][0], primPos[1][1], primPos[1][2])
    #add primitive to file for my BS pipe
    env = environment.Environment()
    curDir = env.get_file_dir(mc.file(q=True, sn=True))[1:]
    f = curDir + '/.prims.txt'
    f = open(f, 'a')
    f.write(selDag + ',' + primPath + '\n')
    f.close()
    #write into second file for stupid maya bug
    ts = time.time()
    stupid_file = "/groups/unfamiliar/modeling/throwaway_txt/" + str(ts).split('.')[0] + '.txt'
    f = open(stupid_file, "w")
    f.write(selDag + ',' + primPath + '\n')
    f.close

    
class mayaRun:
    def run(self):
        replacePrim()
