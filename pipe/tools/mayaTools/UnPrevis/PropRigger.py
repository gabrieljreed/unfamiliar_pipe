import maya.cmds as cmds
import maya.api.OpenMaya as om

class PropRigger():
    def override_color(self, sel, color_index):
        shape =cmds.listRelatives (sel, shapes = True )
        for node in shape:	
            cmds. setAttr (node+".overrideEnabled" ,True) 
            cmds. setAttr (node+".overrideColor" ,color_index)

    def run_er(self):
        sel_list = cmds.ls(sl= True)
        print(sel_list)

        for sel in sel_list:
            bounding_box = cmds.xform(sel, q=1, bb=1, ws=1)
            x_min, y_min, z_min, x_max, y_max, z_max = bounding_box
            pivot = cmds.xform(sel, q=True, rp=True, ws=True)
            rot = cmds.getAttr(sel+'.rotate')

            pv, mx = om.MVector(pivot), om.MVector([x_max, y_max, z_max])
            max_girth = om.MVector(mx-pv).length()



            cmds.select(d=True)
            worldJnt = cmds.joint(p=(0, 0, 0), n = sel+'_worldjnt')
            centerJnt = cmds.joint(p=pivot, o=rot[0], n= sel+'_centerjnt')

            worldCtrl = cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), r = max_girth*3, n = sel+'_worldCtrl')
            centerCtrl = cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), r = max_girth*2, n = sel+'_centerCtrl')
            self.override_color(worldCtrl, 17)
            self.override_color(centerCtrl, 17)
            cmds.setAttr(centerCtrl[0]+'.translate', pivot[0], pivot[1], pivot[2])
            cmds.setAttr(centerCtrl[0]+'.rotate', rot[0][0], rot[0][1], rot[0][2])
            cmds.parent(centerCtrl[0], worldCtrl[0])

            cmds.parentConstraint(worldCtrl[0], worldJnt)
            cmds.parentConstraint(centerCtrl[0], centerJnt)

            if cmds.keyframe(sel, sl=False, q=True, tc=True): # if selected object has keys
                cmds.copyKey(sel, animation='objects', option='keys')
                cmds.pasteKey(centerCtrl[0], animation='objects', option='replaceCompletely')
                cmds.cutKey(sel, s=True)

            cmds.skinCluster(centerJnt, sel, n=sel+'_skinCluster', tsb=True, bm=0, sm=0, nw=1)

#pr = PropRigger()
#pr.run()