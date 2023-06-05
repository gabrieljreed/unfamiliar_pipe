from socket import dup
from tkinter import SEL_LAST
import maya.cmds as cmds
import maya.mel as mel
import functools
import os
import platform


# Import PySide libraries.
#from PySide2 import QtCore
#from PySide2 import QtWidgets

'''TODO: Make the export buttons be inactive when there is no path, name and selection. And reactivate them whenever all three pieces of info 
        are available.'''

GREEN = [11.0/255.0,97.0/255.0,5.0/255.0]
DARKGRAY = [48.0/255.0,48.0/255.0,48.0/255.0]
RED = [0.43, 0.0, 0.0]
LIGHTGRAY = [93.0/255.0,93.0/255.0,93.0/255.0]

class ExportInfo:
    def __init__(self):
        self.att_list = []
    
    def toString(self):
        theString = ''
        for i, att in enumerate(self.att_list):
            theString = theString + '   '+str(i)+') '+att[0]+': '+str(att[1])+'\n'
        return theString
    
    def printContent(self):
        for i, att in enumerate(self.att_list):
            print('   '+str(i)+') '+att[0]+': '+str(att[1]))
    

class CharacterExportInfo(ExportInfo):
    def __init__(self, sel_exp=None, exp_name='', exp_path='', smthGrps=True, smthMesh=True, spltVertNorm=False, triang=False, 
                tangBi=True, skinning=True, blendShapes=True, inConn=True, embTex=True, upAxis='y'):
        attributes = {
            'exportType':'Character',#common
            'selection_export': sel_exp,#common
            'export_name': exp_name,#common
            'export_path':exp_path,#common

            'upAxis': upAxis,#common

            'smoothingGroups': smthGrps,
            'smoothMesh': smthMesh,
            'splitVertexNormals': spltVertNorm,
            'triangulate': triang,
            'tangentsAndBinormals': tangBi,
            'skinning': skinning,
            'blendshapes': blendShapes,
            'inputConnections': inConn,
            'embeddedTextures':embTex
        }
        self.att_list = []
        for key, val in attributes.items():
            subList = [key, val]
            self.att_list.append(subList)
        #print('creating character')
    
    def runTask(self):
        print("running_task")
        print(str(self.att_list[5][1]))
        cmds.select(self.att_list[1][1], r=True, hi=True)
        mel.eval('FBXResetExport')
        mel.eval('FBXExportSmoothingGroups -v '+str(self.att_list[5][1]).lower())
        mel.eval('FBXExportSmoothMesh -v '+str(self.att_list[6][1]).lower())
        mel.eval('FBXExportHardEdges -v '+str(self.att_list[7][1]).lower()) #Split Vertex Normals
        mel.eval('FBXExportTriangulate -v '+str(self.att_list[8][1]).lower())
        mel.eval('FBXExportTangents -v '+str(self.att_list[9][1]).lower()) #Tangents & Binormals
        mel.eval('FBXExportSkins -v '+str(self.att_list[10][1]).lower()) #Skinning
        mel.eval('FBXExportShapes -v '+str(self.att_list[11][1]).lower()) #Blendshapes

        mel.eval('FBXExportInputConnections -v '+str(self.att_list[12][1]).lower())
        mel.eval('FBXExportEmbeddedTextures -v '+str(self.att_list[13][1]).lower())
        mel.eval('FBXExportUpAxis '+str(self.att_list[4][1]))
        exportString = str(self.att_list[3][1])+str(self.att_list[2][1])+'.fbx'
        print(exportString)
        mel.eval('FBXExport -f "{}" -s'.format(exportString))


class CharacterAnimExportInfo(ExportInfo):
    def __init__(self, sel_exp=None, exp_name='', exp_path='', bakeComplexAnim=True, upAxis='y', animStartF=0, animEndF=0):
        attributes = {
            'exportType':'Animation',#common
            'selection_export': sel_exp,#common
            'export_name': exp_name,#common
            'export_path':exp_path,#common
            'upAxis': upAxis,#common
            'bakeComplexAnim': bakeComplexAnim,
            'bakeComplexStart': animStartF,
            'bakeComplexEnd': animEndF
        }
        self.att_list = []
        for key, val in attributes.items():
            subList = [key, val]
            self.att_list.append(subList)
        #print('creating anim')
    
    def runTask(self):
        print("running_task")
        cmds.select(self.att_list[1][1], r=True)
        mel.eval('FBXResetExport')
        mel.eval('FBXExportBakeComplexAnimation -v '+str(self.att_list[5][1]).lower())
        mel.eval('FBXExportUpAxis '+str(self.att_list[4][1]))
        mel.eval('FBXExportBakeComplexStart -v '+str(self.att_list[6][1]))
        mel.eval('FBXExportBakeComplexEnd -v '+str(self.att_list[7][1]))
        exportString = str(self.att_list[3][1])+str(self.att_list[2][1])+'.fbx'
        print(exportString)
        mel.eval('FBXExport -f "{}" -s'.format(exportString))


class PropExportInfo(ExportInfo):
    def __init__(self, sel_exp=None, exp_name='', exp_path='', smthGrps=True, smthMesh=True, spltVertNorm=False, triang=False, 
                tangBi=True, skinning=True, blendShapes=True, inConn=True, embTex=True, bakeComplexAnim=True, upAxis='y', animStartF=0, animEndF=0):
        attributes = {
            'exportType':'Prop',#common
            'selection_export': sel_exp,#common
            'export_name': exp_name,#common
            'export_path':exp_path,#common
            'upAxis': upAxis,#common

            'smoothingGroups': smthGrps,
            'smoothMesh': smthMesh,
            'splitVertexNormals': spltVertNorm,
            'triangulate': triang,
            'tangentsAndBinormals': tangBi,
            'skinning': skinning,
            'blendshapes': blendShapes,
            'inputConnections': inConn,
            'embeddedTextures':embTex,

            'bakeComplexAnim': bakeComplexAnim,
            'bakeComplexStart': animStartF,
            'bakeComplexEnd': animEndF
        }
        self.att_list = []
        for key, val in attributes.items():
            subList = [key, val]
            self.att_list.append(subList)

    def runTask_OLD(self):
        print("running_task")
        cmds.currentTime(1, e=1)
        main_grp = self.att_list[1][1]
        cmds.select(main_grp, r=True)
        grp_lst = []
        jnt_lst = []
        new_grp = cmds.group( em=True, name=str(self.att_list[2][1])+'_temp_duplicate' )
        duplicate = cmds.duplicate(main_grp, rc=True)

        cmds.parent(duplicate[0], new_grp)

        '''cmds.select(duplicate)
        cmds.freeze()
        cmds.select(cl=True)'''

        cmds.select(new_grp, r=True)
        w_joint = cmds.joint(n=main_grp+'_world_jnt', p=(0,0,0))
        self.findJointLocation(main_grp, grp_lst,jnt_lst, None, duplicate, False, 0)
        print(grp_lst, jnt_lst)

        '''par_jnt_pos = []
        for frame in range(int(self.att_list[15][1]), int(self.att_list[16][1])+1):
                cmds.currentTime(frame, e=1)
                for i,s in enumerate(grp_lst):
                    sel_pos = cmds.xform(s,q=1,ws=1,rp=1)
                    sel_rot = cmds.xform(s, q=1, ro=1)
                    #cmds.setAttr(jnt_lst[i]+".translate", sel_pos[0], sel_pos[1], sel_pos[2])
                    if i>0:
                        #print(sel_pos, par_jnt_pos)
                        sel_pos = cmds.getAttr(s+'.translate')[0]#[sel_pos[0]-par_jnt_pos[0],sel_pos[1]-par_jnt_pos[1],sel_pos[2]-par_jnt_pos[2]]
                        print(sel_pos)
                    #cmds.joint(jnt_lst[i],e=True, p=sel_pos)
                    cmds.setAttr(jnt_lst[i]+'.translate', sel_pos[0], sel_pos[1], sel_pos[2])
                    cmds.setAttr(jnt_lst[i]+'.rotate', sel_rot[0], sel_rot[1], sel_rot[2])
                    #print(sel_rot)
                    cmds.setKeyframe(jnt_lst[i])
                    par_jnt_pos = sel_pos'''


        #first check if the group has keyframes
        #then find the actual mesh objects, and check if they have keyframes
        # on the objects that have keyframes, find the center of mass and place a joint
        # skin the objects to that joint
        # transfer the movement of all animated objects to that joint at all frames
        # export the rigged duplicate?
        '''mel.eval('FBXResetExport')

        mel.eval('FBXExportUpAxis '+str(self.att_list[4][1]))

        mel.eval('FBXExportSmoothingGroups -v '+str(self.att_list[5][1]).lower())
        mel.eval('FBXExportSmoothMesh -v '+str(self.att_list[6][1]).lower())
        mel.eval('FBXExportHardEdges -v '+str(self.att_list[7][1]).lower()) #Split Vertex Normals
        mel.eval('FBXExportTriangulate -v '+str(self.att_list[8][1]).lower())
        mel.eval('FBXExportTangents -v '+str(self.att_list[9][1]).lower()) #Tangents & Binormals
        mel.eval('FBXExportSkins -v '+str(self.att_list[10][1]).lower()) #Skinning
        mel.eval('FBXExportShapes -v '+str(self.att_list[11][1]).lower()) #Blendshapes

        mel.eval('FBXExportInputConnections -v '+str(self.att_list[12][1]).lower())
        mel.eval('FBXExportEmbeddedTextures -v '+str(self.att_list[13][1]).lower())

        mel.eval('FBXExportBakeComplexAnimation -v '+str(self.att_list[14][1]).lower())
        mel.eval('FBXExportBakeComplexStart -v '+str(self.att_list[15][1]))
        mel.eval('FBXExportBakeComplexEnd -v '+str(self.att_list[16][1]))
        exportString = str(self.att_list[3][1])+str(self.att_list[2][1])+'.fbx'
        print(exportString)
        mel.eval('FBXExport -f "{}" -s'.format(exportString))'''

    def findJointLocation(self, sel, grp_lst, jnt_lst, loc_list, bind_to_jnt, firstJoint):
        #print("------------------------------------------------------------"+str(i))
        d_sel_name = sel.rsplit(':',1)[1] if ':' in sel else sel
        #print(d_sel_name)
        if cmds.keyframe(sel, query=True, keyframeCount=True) or firstJoint==True: #if sub-mesh has got keyframes
            sel_pos = cmds.xform(sel, q=1, ws=1, rp=1)
            sel_rot = cmds.xform(sel, q=1, ro=1)
            grp_lst.append(d_sel_name)
            sel_jnt = cmds.joint(n=d_sel_name+'_jnt', p=sel_pos, o=sel_rot)
            sel_loc = cmds.spaceLocator(n=d_sel_name+'_loc')
            cmds.parent(sel_loc, sel_jnt)
            cmds.setAttr(sel_loc[0]+'.translate', 0,0,0)
            cmds.setAttr(sel_loc[0]+'.rotate', 0,0,0)
            cmds.parent(sel_loc, sel)
            cmds.parentConstraint(sel_loc, sel_jnt)
            bind_to_jnt = sel_jnt
            jnt_lst.append(sel_jnt)
            loc_list.append(sel_loc[0])

            cmds.select(sel_jnt, r=True)
        sel_children = cmds.listRelatives(sel, type='transform')
        if sel_children:
            par_consts = cmds.listRelatives(sel, type='parentConstraint')
            if par_consts: 
                for pc in par_consts: sel_children.remove(pc)
            for child in sel_children:
                self.findJointLocation(child, grp_lst, jnt_lst, loc_list, bind_to_jnt, False)
    
    def makeSkinningGroups(self, mesh_grp):
        all_shapes = []
        for i,d_k in enumerate(mesh_grp):
            rels = cmds.listRelatives(d_k)
            rels.append(d_k)
            shape_list = []
            exlude_group = mesh_grp.copy()
            exlude_group.remove(d_k)
            for r in rels:
                shape = cmds.listRelatives(r, shapes=True)
                if shape and r not in exlude_group:
                    shape_list.append(r)
            all_shapes.append(shape_list)
        return all_shapes
    
    def skinGroups(self, joints, skins_grp):
        '''print("Skin Groups!!!!!")
        for slist in skins_grp:
            print(str(slist))'''
        #meshes = list(reversed(skins_grp))
        #jnts = list(reversed(joints))
        for i,joint in enumerate(joints):
            #if cmds.objExists(skins_grp[i]+'_skinCluster'):
            #cmds.bindSkin(joint,mesh,n=mesh+'_skinCluster', tsb=True, bcp=True)
            cmds.skinCluster(joint, skins_grp[i][0], n=skins_grp[i][0]+'_skinCluster', tsb=True, bm=1, sm=0, nw=0)  

    def runTask(self):
        main_grp = self.att_list[1][1]
        cmds.select(main_grp, r=True)
        grp_lst = []
        jnt_lst = []
        loc_lst = [] #delete all of these locs too
        new_grp = cmds.group( em=True, name=str(self.att_list[2][1])+'_temp_duplicate' ) # select to delete everything
        mesh_grp = cmds.group( em=True, name=str(self.att_list[2][1])+'_mesh') #select the mesh grp to export
        cmds.parent(mesh_grp, new_grp)
        duplicate = cmds.duplicate(main_grp, rc=True)
        cmds.parent(duplicate[0], mesh_grp)
        cmds.select(new_grp, r=True)
        w_joint = cmds.joint(n=main_grp+'_world_jnt', p=(0,0,0)) # select this joint to export

        self.findJointLocation(main_grp, grp_lst,jnt_lst, loc_lst,  None, True)
        #print(str(grp_lst)+'\n'+str(jnt_lst)+'\n'+str(loc_lst))

        dup_mesh_grp = []
        for grp in grp_lst:
            dup = [s for s in duplicate if grp in s]
            if dup:
                dup_mesh_grp.append(dup[0])

        skin_grps = self.makeSkinningGroups(dup_mesh_grp)

        #reset_parenting
        #print(duplicate)
        #print(duplicate)
        #print(len(duplicate))
        if len(duplicate) > 1:
            cmds.parent(duplicate, mesh_grp)
        for dup in duplicate:
            shape = cmds.listRelatives(dup, shapes=True)
            if not shape: cmds.delete(dup)
        
        self.skinGroups(jnt_lst, skin_grps)
        self.exportFBX(new_grp, mesh_grp, w_joint, loc_lst)
    
    def exportFBX(self, new_grp, mesh_grp, w_joint, loc_lst):

        cmds.select(w_joint, r=True)
        cmds.select(mesh_grp, add=True)
        
        #cmds.cacheEvaluator(flushCache='destroy')
        #cmds.cacheEvaluator(cacheFillMode = 'syncAsync')
        #cmds.cacheEvaluator(query=True, safeModeMessages=True)
        #cmds.cacheEvaluator(waitForCache=10) #chache wait command!!!!!!!!
        #cmds.pause( sec=10 )

        mel.eval('FBXResetExport')
        mel.eval('FBXExportUpAxis '+str(self.att_list[4][1]))
        mel.eval('FBXExportSmoothingGroups -v '+str(self.att_list[5][1]).lower())
        mel.eval('FBXExportSmoothMesh -v '+str(self.att_list[6][1]).lower())
        mel.eval('FBXExportHardEdges -v '+str(self.att_list[7][1]).lower()) #Split Vertex Normals
        mel.eval('FBXExportTriangulate -v '+str(self.att_list[8][1]).lower())
        mel.eval('FBXExportTangents -v '+str(self.att_list[9][1]).lower()) #Tangents & Binormals
        mel.eval('FBXExportSkins -v '+str(self.att_list[10][1]).lower()) #Skinning
        mel.eval('FBXExportShapes -v '+str(self.att_list[11][1]).lower()) #Blendshapes

        mel.eval('FBXExportInputConnections -v '+str(self.att_list[12][1]).lower())
        mel.eval('FBXExportEmbeddedTextures -v '+str(self.att_list[13][1]).lower())

        mel.eval('FBXExportBakeComplexAnimation -v '+str(self.att_list[14][1]).lower())
        mel.eval('FBXExportBakeComplexStart -v '+str(self.att_list[15][1]))
        mel.eval('FBXExportBakeComplexEnd -v '+str(self.att_list[16][1]))
        exportString = str(self.att_list[3][1])+str(self.att_list[2][1])+'.fbx'
        print(exportString)
        mel.eval('FBXExport -f "{}" -s'.format(exportString))

        #delete temp duplicate group and locators stuff
        cmds.delete(new_grp)
        cmds.delete(loc_lst)


class CameraExportInfo(ExportInfo):
    def __init__(self, sel_exp=None, exp_name='', exp_path='', bakeComplexAnim=True, upAxis='y'):
        attributes = {
            'exportType':'Camera',
            'selection_export': sel_exp,
            'export_name': exp_name,
            'export_path':exp_path,
            'upAxis': upAxis,
            'bakeComplexAnim': bakeComplexAnim
        }
        self.att_list = []
        for key, val in attributes.items():
            subList = [key, val]
            self.att_list.append(subList)


class SceneData():
    def __init__(self):
        print('collecting data')
        self.filename = ''

        self.animStartF = int(cmds.playbackOptions(q=True,animationStartTime=True))
        self.animEndF = int(cmds.playbackOptions(q=True,animationEndTime=True))
        self.minTimeF = int(cmds.playbackOptions(q=True,minTime=True))
        self.maxTimeF = int(cmds.playbackOptions(q=True,maxTime=True))

        self.shotExportPath, self.propExportPath = self.createMayaExportPaths()
        self.charUnrealExports = self.getCharacterExportSets()
        self.propUnrealExports = self.getPropExportSets()
        self.charAnimFbxExportInfoList = self.createCharacterAnimExportList()
        self.propAnimFbxExportInfoList = self.createPropAnimExportList()
        self.allExportsList = self.charAnimFbxExportInfoList + self.propAnimFbxExportInfoList
    
    def createMayaExportPaths(self):
        print(platform.system()) #'Windows' or 'Linux'
        split_char='/'
        """if platform.system() == 'Windows':
            split_char='\\'"""

        currdir = cmds.file(q=True, sn=True)
        self.filename = ''
        print(currdir)
        if os.path.isfile(currdir):
                sep = currdir.rsplit(split_char,1)
                currdir = sep[0]
                self.filename = sep[1].rsplit('.',1)[0]
        newdir_char = currdir+split_char+self.filename+'_ExportsUE'+split_char+'character_animations'
        newdir_prop = currdir+split_char+self.filename+'_ExportsUE'+split_char+'prop_animations'
        if not os.path.exists(newdir_char):
                os.makedirs(newdir_char)
        if not os.path.exists(newdir_prop):
                os.makedirs(newdir_prop)
        ds = newdir_char+split_char
        ds2 = newdir_prop+split_char
        return ds.replace('\\','/'), ds2.replace('\\','/')# for maya pathing purposes
    
    def list_filter(self, string, substr):
        return [str for str in string if any(sub in str for sub in substr)]
    
    def getCharacterExportSets(self):
        foundSets=self.list_filter(cmds.ls(exactType="objectSet"),['UnrealExport'])# key word here is UnrealExport
        return foundSets
    
    def createCharacterAnimExportList(self):
        charAnimList = []
        for char in self.charUnrealExports:
            expName = self.filename+'_'+char.split(':')[0]+'_Animation'
            charAnim = CharacterAnimExportInfo(sel_exp = char, exp_name = expName, exp_path = self.shotExportPath, animStartF=self.animStartF, animEndF=self.animEndF)
            charAnimList.append(charAnim)
        return charAnimList
    
    def getPropExportSets(self):
        all_props = []
        if cmds.objExists('Props'):
            all_props=cmds.listRelatives('Props', c=True)# MAKE MAIN GROUP IS 'Props'

        #for f_set in foundSets:
        #    all_props = all_props + cmds.sets(f_set, query=True, nodesOnly=True)
        return all_props
    
    def createPropAnimExportList(self):
        propAnimList = []
        for prop in self.propUnrealExports:
            expName = self.filename+'_'+prop+'_Animation'
            propAnim = PropExportInfo(sel_exp = prop, exp_name = expName, exp_path = self.propExportPath, animStartF=self.animStartF, animEndF=self.animEndF)
            propAnimList.append(propAnim)
        return propAnimList


class MR_Window(): 
    #constructor
    def __init__(self, sceneData):
            
        self.window = 'MR_Window'
        self.title = 'Unreal FBX Exporter'
        self.size = (550, 400)
        self.allData = sceneData

        self.tabNum = 0

        # close old window is open
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
            
        #create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.scrollLayout = cmds.scrollLayout( horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
        self.mainLayout = cmds.columnLayout()#(cal="center")
        
        ### creating optionMenu
        '''cmds.optionMenu( label='Select Character Set', changeCommand= self.printNewMenuItem )
        for item in self.allData.charUnrealExports:
            cmds.menuItem( label=item )'''
        ### end creation option menu
        
        self.taskLayout = cmds.columnLayout(parent = self.mainLayout)
        #self.createLayoutTest()
        self.allTasks = []


        self.buttonsLayout = cmds.rowLayout(numberOfColumns=3, vis=True, columnWidth3=(550/3, 550/3, 550/3), columnAlign3=['center','center','center'], parent=self.mainLayout)

        buttonlen = 180
        cmds.button (label = "Add Task", w = buttonlen, h = 30, al='center', bgc = [0.0,0.0,0.0], 
                    command=functools.partial(self.createTaskTest), parent = self.buttonsLayout)
        cmds.button (label = "Clear Tasks", w = buttonlen, h = 30, al='center', bgc = [0.0,0.0,0.0], 
                    command=functools.partial(self.clearAllTasks), parent = self.buttonsLayout)
        cmds.button (label = "Batch Export", w = buttonlen, h = 30, al='center', bgc = [0.0,0.0,0.0], 
                    command=functools.partial(self.batchExport), parent = self.buttonsLayout)
        
        #create the animation tasks for me!!!
        for c in self.allData.allExportsList:
            self.tabNum = self.tabNum+1
            new_task = Task_Component(taskLayout=self.taskLayout, taskNum=self.tabNum, sceneData=self.allData, objInfoIn=c, windowData=self)
            self.allTasks.append(new_task)

        #display new window
        cmds.showWindow()
    
    def createTaskTest(self,*pArgs):
        self.tabNum = self.tabNum+1
        curr_task = Task_Component(taskLayout=self.taskLayout, taskNum=self.tabNum, sceneData=self.allData, windowData=self)
        self.allTasks.append(curr_task)
    
    def checkOutTest(self, *pArgs):
        print(len(self.allTasks))
        for t in self.allTasks:
            print('t.TaskCompleted: '+str(t.TaskCompleted)+'; t.Exportable: '+str(t.Exportable))
    
    def clearAllTasks(self, *pArgs):
        for t in self.allTasks:
            t.deleteTaskItem(True)
        self.allTasks.clear()
        self.tabNum = 0
    
    def batchExport(self, *pArgs):
        for t in self.allTasks:
            if t.Exportable == True and t.TaskCompleted == False:
                t.exportButtonPressed()


class Task_Component(): 
    #constructor
    def __init__(self, taskLayout, taskNum, sceneData, objInfoIn = None, windowData = None):
        self.allData = sceneData
        self.CharacterInfo = CharacterExportInfo()#charInfo
        self.AnimationInfo = CharacterAnimExportInfo(animStartF=self.allData.minTimeF, animEndF=self.allData.maxTimeF)#animInfo
        self.PropInfo = PropExportInfo(animStartF=self.allData.minTimeF, animEndF=self.allData.maxTimeF)#propInfo
        self.CameraInfo = CameraExportInfo()#camInfo
        self.DataToExport = None
        self.ParentWindowData = windowData

        self.Exportable = False
        self.TaskCompleted = False

        self.initialArr = [1,0,0,0]
        self.TaskToggleList = []
        self.TaskToggleListStartIndex = 5 # for now, since after upAxis, all variables are diff
        self.taskNum = taskNum
        if objInfoIn != None:
            self.objInfoDetermine(objInfoIn) # to copy to the right info save
        else:
            self.DataToExport = self.CharacterInfo

        self.row_layout = cmds.rowLayout(numberOfColumns=2,columnWidth2=(500, 30), parent=taskLayout)
        self.task_title = "Task "+str(self.taskNum)+": "+str(self.DataToExport.att_list[1][1])+" "+self.DataToExport.att_list[0][1]+" Export"
        self.frameLayout1 = cmds.frameLayout (width = 500, label = self.task_title, collapse = True, collapsable = True, 
                                        marginWidth = 5, parent = self.row_layout)
        #delete task button
        cmds.button (label='Delete', command=functools.partial(self.deleteTaskItem), parent=self.row_layout, 
                    bgc=RED)
        
        subFrameLayout = cmds.columnLayout(parent=self.frameLayout1)# this might be useless

        #radioButton for type of export
        self.sel_ex_type_layout = cmds.rowLayout(numberOfColumns=4, vis=True, columnWidth4=(500/4, 500/4, 500/4, 500/4), columnAlign4=['center','center','center','center'], 
                                                parent=subFrameLayout)
        menucontainer = cmds.formLayout(parent=subFrameLayout)

        char_layout = cmds.columnLayout(ann='Character', vis=self.initialArr[0], parent=menucontainer)
        self.characterMenu(char_layout)
        
        anim_layout = cmds.columnLayout(ann='Animation', vis=self.initialArr[1], parent=menucontainer)
        self.animationMenu(anim_layout)

        prop_layout = cmds.columnLayout(ann='Prop', vis=self.initialArr[2], parent = menucontainer)
        self.propMenu(prop_layout)

        cam_layout = cmds.columnLayout(ann='Camera', vis=self.initialArr[3], parent=menucontainer)
        self.cameraMenu(cam_layout)

        #exception for message
        self.exported_message_layout = cmds.columnLayout(ann='Message', vis = False, parent=menucontainer)
        center_rowLay = cmds.rowLayout(numberOfColumns=3, columnWidth3=(300*(1/10), 300*(8/3), 300*(1/10)), columnAlign3=['center','center','center'], parent=self.exported_message_layout)
        cmds.text(label='', align= 'left', parent=center_rowLay)
        #scroll field for export message
        self.exportScrollField = cmds.scrollField(text=self.task_title+'\n'+self.DataToExport.toString(), 
                        w=400, h=100, parent=center_rowLay) #wordWrap=True

        self.menuLayout_list = [char_layout, anim_layout, prop_layout, cam_layout]

        self.exp_type_radColl = cmds.radioCollection(parent = subFrameLayout)
        cmds.radioButton( label='Character', sl=self.initialArr[0], onCommand=functools.partial(self.changeTypeMenu), parent=self.sel_ex_type_layout)
        cmds.radioButton( label='Animation', sl=self.initialArr[1], onCommand=functools.partial(self.changeTypeMenu), parent=self.sel_ex_type_layout)
        cmds.radioButton( label='Prop', sl=self.initialArr[2], onCommand=functools.partial(self.changeTypeMenu), parent=self.sel_ex_type_layout)
        cmds.radioButton( label='Camera', sl=self.initialArr[3], onCommand=functools.partial(self.changeTypeMenu), parent=self.sel_ex_type_layout)
        #cmds.button (label = "Task", w = 280, h = 50, command='print("task button!")', parent=taskLayout)

    def updateExportMessage(self):
        cmds.scrollField(self.exportScrollField, edit=True, text=self.task_title+'\n'+self.DataToExport.toString()) #wordWrap=True

    #determines what kind of task was the passed task argument
    def objInfoDetermine(self, objInfoIn):
        exportType = objInfoIn.att_list[0][1]
        if exportType == 'Character':
            self.CharacterInfo = objInfoIn
            self.initialArr = [1,0,0,0]
        elif exportType == 'Animation':
            self.AnimationInfo = objInfoIn
            self.initialArr = [0,1,0,0]
        elif exportType == 'Prop':
            self.PropInfo = objInfoIn
            self.initialArr = [0,0,1,0]
        else:
            self.CameraInfo = objInfoIn
            self.initialArr = [0,0,0,1]
        self.DataToExport = objInfoIn

    #deletes a task
    def deleteTaskItem(self, batchDelete=False, *pArgs):
        cmds.deleteUI(self.row_layout)
        if not batchDelete: # if deleting one by one
            self.ParentWindowData.allTasks.remove(self)
    
    #This function allows the task to change menu depending on the choosen functionality. If
    # character export was choosen, the menu will change to a character export menu. If it was
    # animation export, the menu will change to anim export menu. And so on and so forth.
    def changeTypeMenu(self, *pArgs):
        radioCol = cmds.radioCollection(self.exp_type_radColl, query=True, sl=True)
        getSelectRadioVal = cmds.radioButton(radioCol, query=True, label=True)

        infoList = [self.CharacterInfo, self.AnimationInfo, self.PropInfo, self.CameraInfo]
        for i, menu in enumerate(self.menuLayout_list):
            annon = cmds.columnLayout(menu, query=True, ann=True)
            #print("getSelectRadioVal: "+getSelectRadioVal+" |vs| menu-annon: "+annon)
            if getSelectRadioVal == annon:
                self.DataToExport = infoList[i]
                cmds.columnLayout(menu, edit=True, vis=True)
            else:
                cmds.columnLayout(menu, edit=True, vis=False)
        
        self.replaceTaskTitle()
        self.Exportable = self.getExportButtonCondition(self.DataToExport)
        frameLayoutColor = GREEN if self.Exportable else LIGHTGRAY
        cmds.frameLayout(self.frameLayout1, edit=True, bgc=frameLayoutColor)
    
    #This function takes a character select menu and arranges the default menu setting for
    # the character selecter in case the encompasing SceneData object commands a task to choose
    # a character; this will also call a function that will update it's export button
    def updateOptionMenu(self, optionMenu, exportObject, exportButton):#do button later
        setCharacter = exportObject.att_list[1][1]
        sel_index = 1

        if setCharacter != None:
            options_list = cmds.optionMenu(optionMenu, query=True, itemListShort=True)
            for i, option in enumerate(options_list):
                if setCharacter == cmds.menuItem(option, query=True, label=True):
                    sel_index = i+1

        cmds.optionMenu(optionMenu, edit=True, sl=sel_index, changeCommand=functools.partial(self.setObjectFromMenuItem, optionMenu, exportObject, exportButton))
     
    def updateFilePath(self, inputFieldPath, findPathButton, exportObject, exportButton):
        cmds.button(findPathButton, edit=True, command=functools.partial(self.findFilePathPrompt, inputFieldPath, exportObject, 3, exportButton)) #index 3 is file

    def updateExportName(self, inputFieldName, exportObject, exportButton):
        cmds.textField(inputFieldName, edit=True, cc=functools.partial(self.saveChangedText, inputFieldName, exportObject, 2, exportButton)) #index 2 is export name
    
    def checkIfButtonEnabled(self, exportObject, exportButton):
        exportCond = self.getExportButtonCondition(exportObject)
        self.Exportable = exportCond
        cmds.button(exportButton, edit=True, enable= exportCond)
        frameLayoutColor = GREEN if self.Exportable else LIGHTGRAY
        cmds.frameLayout(self.frameLayout1, edit=True, bgc=frameLayoutColor)


    def setObjectFromMenuItem(self, objOptionMenu, exportObject, exportButton, *pArgs):
        item = cmds.optionMenu(objOptionMenu, q=True, v=True)
        #print ( "setObjectFromMenuItem: "+item )
        if item == 'Selection':
            exportObject.att_list[1][1] = cmds.ls(sl=True)
        else:
            exportObject.att_list[1][1] = item
        self.replaceTaskTitle()
        self.checkIfButtonEnabled(exportObject, exportButton)

    def findFilePathPrompt(self, inputField, exportObject, index, exportButton, *pArgs):
        try:
            task_export_path = cmds.fileDialog2(fileMode=3, dialogStyle=1, caption="Choose the fbx export location: ")[0]+'/'
        except:
            task_export_path = ''
        cmds.textField(inputField, edit=True, tx=task_export_path)
        exportObject.att_list[index][1] = task_export_path
        self.checkIfButtonEnabled(exportObject, exportButton)

    def saveChangedText(self, inputField, exportObject, index, exportButton, *pArgs):
        #print(cmds.textField(inputField, query=True, text=True))
        exportObject.att_list[index][1] = cmds.textField(inputField, query=True, text=True)
        self.checkIfButtonEnabled(exportObject, exportButton)
    
    #gets current button conditions
    def getExportButtonCondition(self, exportObject):
        #indexes 1,2 and 3
        i1, i2, i3 = True, True, True
        #print(' ')
        #print('selection: '+str(exportObject.att_list[1][1]))
        if exportObject.att_list[1][1] == '' or exportObject.att_list[1][1] == None: #if no selection
            i1 = False
        #print('name: '+str(exportObject.att_list[2][1]))
        if exportObject.att_list[2][1] == '' or exportObject.att_list[2][1] == None: #if no export name
            i2 = False
        #print('path: '+str(exportObject.att_list[3][1]))
        if exportObject.att_list[3][1] == '' or exportObject.att_list[3][1] == None: #if no export path
            i3 = False
        #print(i1,i2,i3)
        return all(c==True for c in [i1,i2,i3])

    def createFilePathContainer(self, exportObject, parentContainer):
        searchFilePathContainer = cmds.rowLayout(parent=parentContainer, nc=3)
        cmds.text(label='Export Path: ', align= 'left', parent=searchFilePathContainer)
        inputFieldPath = cmds.textField(tx=exportObject.att_list[3][1], ed=False, w=360, parent=searchFilePathContainer)
        findPathButton = cmds.button(label='find path', w=60, h=20, parent=searchFilePathContainer)
        return inputFieldPath, findPathButton
    
    def createFileNameContainer(self, exportObject, parentContainer):
        fileNameContainer = cmds.rowLayout(parent=parentContainer, nc=3)
        cmds.text(label='Export Name: ', align= 'left', parent=fileNameContainer)
        inputFieldName = cmds.textField(tx=exportObject.att_list[2][1], ed=True, w=360, parent=fileNameContainer)
        cmds.textField(tx='.fbx', ed=False, w=60, parent=fileNameContainer)
        return inputFieldName


    #Creates the character export menu
    def characterMenu(self, parentContainer):
        #This creates the character selection optionMenu
        charOptionMenu = cmds.optionMenu( label='Select Character Set', parent=parentContainer)
        cmds.menuItem(label='Selection')
        for item in self.allData.charUnrealExports:
            cmds.menuItem( label=item )
        
        #creating filepath container objects
        charInputFieldPath, charFindPathButton =  self.createFilePathContainer(self.CharacterInfo, parentContainer)
        #creating export name container objects
        charInputFieldName = self.createFileNameContainer(self.CharacterInfo, parentContainer)
        
        char_checkBoxInfo = [p[1] for p in self.CharacterInfo.att_list[5::]] # from index 5
        cmds.checkBox( label='Smoothing Groups', value=char_checkBoxInfo[0], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 0), 
                                parent=parentContainer)
        cmds.checkBox( label='Smooth Mesh', value=char_checkBoxInfo[1], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 1), 
                                parent=parentContainer)
        cmds.checkBox( label='Split Vertex Normals', value=char_checkBoxInfo[2], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 2), 
                                parent=parentContainer)
        cmds.checkBox( label='Triangulate', value=char_checkBoxInfo[3], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 3), 
                                parent=parentContainer)
        cmds.checkBox( label='Tangent and Binormals', value=char_checkBoxInfo[4], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 4), 
                                parent=parentContainer)
        cmds.checkBox( label='Skinning', value=char_checkBoxInfo[5], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 5), 
                                parent=parentContainer)
        cmds.checkBox( label='Blendshapes', value=char_checkBoxInfo[6], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 6), 
                                parent=parentContainer)
        cmds.separator( h= 10, style= 'none', parent=parentContainer)
        cmds.checkBox( label='Input Connections', value=char_checkBoxInfo[7], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 7), 
                                parent=parentContainer)
        cmds.checkBox( label='Embedded Textures', value=char_checkBoxInfo[8], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, char_checkBoxInfo, 8), 
                                parent=parentContainer)
        cmds.separator( h= 10, style= 'none', parent=parentContainer)
        self.ExportUpAxisRadioColl(parentContainer, self.CharacterInfo)

        center_rowLay = cmds.rowLayout(numberOfColumns=3, columnWidth3=(300/3, 300/3, 300/3), columnAlign3=['center','center','center'], parent=parentContainer)
        cmds.text(label='', align= 'left', parent=center_rowLay)
        
        charMenuExportButton = cmds.button (label='Export Individually', enable=False, w=280, h=25,parent=center_rowLay) 
        self.checkIfButtonEnabled(self.DataToExport, charMenuExportButton)
        
        self.updateOptionMenu(charOptionMenu, self.CharacterInfo, charMenuExportButton)
        self.updateFilePath(charInputFieldPath, charFindPathButton, self.CharacterInfo, charMenuExportButton)
        self.updateExportName(charInputFieldName, self.CharacterInfo, charMenuExportButton)
        
        cmds.button(charMenuExportButton, edit=True, command=functools.partial(self.exportButtonPressed))

    #Creates the animation export menu
    def animationMenu(self, parentContainer):
        #this creates the anim character selection optionMenu
        animCharOption = cmds.optionMenu( label='Select Character Set', parent=parentContainer)
        cmds.menuItem(label='Selection')
        for item in self.allData.charUnrealExports:
            cmds.menuItem( label=item )

        #creating filepath container objects
        animInputFieldPath, animFindPathButton =  self.createFilePathContainer(self.AnimationInfo, parentContainer)
        #creating export name container objects
        animInputFieldName = self.createFileNameContainer(self.AnimationInfo, parentContainer)
        
        #anim checkbox
        anim_checkBoxInfo = [p[1] for p in self.AnimationInfo.att_list[5::]] # from index 5
        cmds.checkBox( label='Bake Complex Animation', value=anim_checkBoxInfo[0], 
                        changeCommand=functools.partial(self.checkBoxChangeInfo, anim_checkBoxInfo, 0),
                        parent=parentContainer)
        
        bASF_container = cmds.rowLayout(parent=parentContainer, nc=2)
        cmds.text(label='Bake Complex Animation Start Frame: ', align= 'left', parent=bASF_container)
        bakeAnimStartField = cmds.textField(tx=anim_checkBoxInfo[1], ed=True, w=50, parent=bASF_container)
        cmds.textField(bakeAnimStartField, edit=True, cc=functools.partial(self.checkNumberChangeInfo, anim_checkBoxInfo, bakeAnimStartField, 1))
        
        bAEF_container = cmds.rowLayout(parent=parentContainer, nc=2)
        cmds.text(label='Bake Complex Animation Start Frame: ', align= 'left', parent=bAEF_container)
        bakeAnimEndField = cmds.textField(tx=anim_checkBoxInfo[2], ed=True, w=50, parent=bAEF_container)
        cmds.textField(bakeAnimEndField, edit=True, cc=functools.partial(self.checkNumberChangeInfo, anim_checkBoxInfo, bakeAnimEndField, 2))
        
        cmds.separator( h= 10, style= 'none', parent=parentContainer)
        self.ExportUpAxisRadioColl(parentContainer, self.AnimationInfo)

        center_rowLay = cmds.rowLayout(numberOfColumns=3, columnWidth3=(300/3, 300/3, 300/3), columnAlign3=['center','center','center'], parent=parentContainer)
        cmds.text(label='', align= 'left', parent=center_rowLay)
        
        animMenuExportButton = cmds.button (label='Export Individually', enable=False, w=280, h=25, parent=center_rowLay)
        self.checkIfButtonEnabled(self.DataToExport, animMenuExportButton)

        self.updateOptionMenu(animCharOption, self.AnimationInfo, animMenuExportButton)
        self.updateFilePath(animInputFieldPath, animFindPathButton, self.AnimationInfo, animMenuExportButton)
        self.updateExportName(animInputFieldName, self.AnimationInfo, animMenuExportButton)

        cmds.button(animMenuExportButton, edit=True, command=functools.partial(self.exportButtonPressed))
         
    #Creates the prop export menu
    def propMenu(self, parentContainer):
        #This creates the character selection optionMenu
        propOptionMenu = cmds.optionMenu( label='Select Prop', parent=parentContainer)
        cmds.menuItem(label='Selection')
        for item in self.allData.propUnrealExports:
            cmds.menuItem( label=item )

        #creating filepath container objects
        propInputFieldPath, propFindPathButton =  self.createFilePathContainer(self.PropInfo, parentContainer)
        #creating export name container objects
        propInputFieldName = self.createFileNameContainer(self.PropInfo, parentContainer)

        prop_checkBoxInfo = [p[1] for p in self.PropInfo.att_list[5::]] # from index 5
        cmds.checkBox( label='Smoothing Groups', value=prop_checkBoxInfo[0], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 0), 
                                parent=parentContainer)
        cmds.checkBox( label='Smooth Mesh', value=prop_checkBoxInfo[1], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 1), 
                                parent=parentContainer)
        cmds.checkBox( label='Split Vertex Normals', value=prop_checkBoxInfo[2], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 2), 
                                parent=parentContainer)
        cmds.checkBox( label='Triangulate', value=prop_checkBoxInfo[3], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 3), 
                                parent=parentContainer)
        cmds.checkBox( label='Tangent and Binormals', value=prop_checkBoxInfo[4], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 4), 
                                parent=parentContainer)
        cmds.checkBox( label='Skinning', value=prop_checkBoxInfo[5], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 5), 
                                parent=parentContainer)
        cmds.checkBox( label='Blendshapes', value=prop_checkBoxInfo[6], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 6), 
                                parent=parentContainer)
        cmds.separator( h= 10, style= 'none', parent=parentContainer)
        cmds.checkBox( label='Input Connections', value=prop_checkBoxInfo[7], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 7), 
                                parent=parentContainer)
        cmds.checkBox( label='Embedded Textures', value=prop_checkBoxInfo[8], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 8), 
                                parent=parentContainer)
        cmds.checkBox( label='Bake Complex Animation', value=prop_checkBoxInfo[9], 
                                changeCommand=functools.partial(self.checkBoxChangeInfo, prop_checkBoxInfo, 9),
                                parent=parentContainer)
        
        bASF_container = cmds.rowLayout(parent=parentContainer, nc=2)
        cmds.text(label='Bake Complex Animation Start Frame: ', align= 'left', parent=bASF_container)
        bakeAnimStartField = cmds.textField(tx=prop_checkBoxInfo[10], ed=True, w=50, parent=bASF_container)
        cmds.textField(bakeAnimStartField, edit=True, cc=functools.partial(self.checkNumberChangeInfo, prop_checkBoxInfo, bakeAnimStartField, 10))
        
        bAEF_container = cmds.rowLayout(parent=parentContainer, nc=2)
        cmds.text(label='Bake Complex Animation Start Frame: ', align= 'left', parent=bAEF_container)
        bakeAnimEndField = cmds.textField(tx=prop_checkBoxInfo[11], ed=True, w=50, parent=bAEF_container)
        cmds.textField(bakeAnimEndField, edit=True, cc=functools.partial(self.checkNumberChangeInfo, prop_checkBoxInfo, bakeAnimEndField, 11))

        cmds.separator( h= 10, style= 'none', parent=parentContainer)
        self.ExportUpAxisRadioColl(parentContainer, self.PropInfo)

        center_rowLay = cmds.rowLayout(numberOfColumns=3, columnWidth3=(300/3, 300/3, 300/3), columnAlign3=['center','center','center'], parent=parentContainer)
        cmds.text(label='', align= 'left', parent=center_rowLay)
        
        propMenuExportButton = cmds.button (label='Export Individually', w=280, h=25, parent=center_rowLay)
        self.checkIfButtonEnabled(self.DataToExport, propMenuExportButton)

        self.updateOptionMenu(propOptionMenu, self.PropInfo, propMenuExportButton)
        self.updateFilePath(propInputFieldPath, propFindPathButton, self.PropInfo, propMenuExportButton)
        self.updateExportName(propInputFieldName, self.PropInfo, propMenuExportButton)

        cmds.button(propMenuExportButton, edit=True, command=functools.partial(self.exportButtonPressed))

    #Creates the camera export menu (MIGHT DELETE LATER)
    def cameraMenu(self, parentContainer):
        center_rowLay = cmds.rowLayout(numberOfColumns=3, columnWidth3=(300/3, 300/3, 300/3), columnAlign3=['center','center','center'], parent=parentContainer)
        cmds.text(label='', align= 'left', parent=center_rowLay)
        cam_button = cmds.button (label='Camera', w=280, h=25, command='print("mom get the camera!!!")', parent=center_rowLay)
    
    def ExportUpAxisRadioColl(self, parentContainer, exportObject):
        cmds.text(label='Up Axis', align= 'left', parent=parentContainer)
        chooseUpAxis_container = cmds.rowLayout(numberOfColumns=3, columnWidth3=(100/3, 100/3, 100/3), parent=parentContainer)
        chooseUpAxis_radColl = cmds.radioCollection()
        orientInfo = self.getOrientInfo(exportObject)
        cmds.radioButton( label='X', sl=orientInfo[0], onCommand=functools.partial(self.changeUpAxis, chooseUpAxis_radColl, exportObject, 4), parent=chooseUpAxis_container)
        cmds.radioButton( label='Y', sl=orientInfo[1], onCommand=functools.partial(self.changeUpAxis, chooseUpAxis_radColl, exportObject, 4), parent=chooseUpAxis_container)
        cmds.radioButton( label='Z', sl=orientInfo[2], onCommand=functools.partial(self.changeUpAxis, chooseUpAxis_radColl, exportObject, 4), parent=chooseUpAxis_container)

    def getOrientInfo(self, exportObject):
        if exportObject.att_list[4][1] == 'x':
            return [1,0,0]
        elif exportObject.att_list[4][1] == 'y':
            return [0,1,0]
        else:
            return [0,0,1]

    def changeUpAxis(self, chooseUpAxis_radColl, exportObject, index, *pArgs):
        radioCol = cmds.radioCollection(chooseUpAxis_radColl, query=True, sl=True)
        getSelectRadioVal = cmds.radioButton(radioCol, query=True, label=True)
        exportObject.att_list[index][1] = getSelectRadioVal.lower()
    
    def checkBoxChangeInfo(self, checkboxList, index, *pArgs):
        checkboxList[index] = not checkboxList[index]
        self.TaskToggleList = checkboxList
    
    def checkNumberChangeInfo(self, checkboxList, numberField, index, *pArgs):
        checkboxList[index] = cmds.textField(numberField, query=True, text=True)
        self.TaskToggleList = checkboxList
    
    def exposeMessage(self):
        cmds.frameLayout(self.frameLayout1, edit=True, bgc=DARKGRAY)
        cmds.rowLayout(self.sel_ex_type_layout, edit=True, vis=False)
        for i, menu in enumerate(self.menuLayout_list):
            cmds.columnLayout(menu, edit=True, vis=False)
        cmds.columnLayout(self.exported_message_layout, edit=True, vis=True)
    
    def replaceTaskTitle(self, *pArgs):
        toTaskT = str(self.DataToExport.att_list[1][1])
        if '[' in toTaskT:
            toTaskT = 'Selection'
        self.task_title = "Task "+str(self.taskNum)+": "+toTaskT+" "+self.DataToExport.att_list[0][1]+" Export"
        cmds.frameLayout(self.frameLayout1, edit=True, label = self.task_title)

    def exportButtonPressed(self, *pArgs):
        print("________________exporting________________")
        #print(checkBoxList)
        #print(checkBoxStartIndex)
        for i, checkbox in enumerate(self.TaskToggleList):
            self.DataToExport.att_list[i+self.TaskToggleListStartIndex][1] = checkbox
        print(self.DataToExport.toString())
        self.updateExportMessage()
        self.DataToExport.runTask() #the one that runs the export task!!!!!
        self.exposeMessage()
        self.TaskCompleted = True

class UnrealExporter():
    def run(self):
        allData = SceneData()  
        for c in allData.allExportsList:
            c.printContent()
            print("___________________________")                              
        myWindow = MR_Window(allData)
        #print(allData.charUnrealExports)
ue = UnrealExporter()
ue.run()