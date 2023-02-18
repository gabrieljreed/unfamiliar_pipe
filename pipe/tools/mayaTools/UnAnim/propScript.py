from functools import partial
import maya.cmds as cmds

props = ['kelleth_doll', 'maggie_doll', 'singe_doll', 'wand', 'ring', 'ring_box', 'bouquet', 'frog', 'kelleth_doll_head']
parent_grp = ['kelleth_doll_main:kelleth_doll_main_CTRL_GRP','maggie_doll_main:maggie_doll_main_CTRL_GRP', 'singe_doll_main:singe_main_CTRL_GRP', 'wand_main:wand_global_ctrl_grp_01', 'ring_n_box_main:ring_ctrl_01_cons', 'ring_n_box_main:ring_box_ctrl_01_cons', 'bouquet_main:bouquet_main_ctrl_grp','7', 'kelleth_doll_main:head_broken_const_grp']
active_parent = parent_grp[0]
active_const = 'Parent'
offset = False

def setOffset(item):
    global offset
    offset = item

def setConst(item):
    global active_const
    active_const = item
    

def setProp(item):
    global active_parent
    if item == 'Kelleth Doll':
        active_parent = parent_grp[0]
    elif item == 'Kelleth Doll Head':
        active_parent = parent_grp[8]
    elif item == 'Maggie Doll':
        active_parent = parent_grp[1]
    elif item == 'Singe Doll':
        active_parent = parent_grp[2]
    elif item == 'Wand':
        active_parent = parent_grp[3]
    elif item == 'Ring':
        active_parent = parent_grp[4]
    elif item == 'Ring Box':
        active_parent = parent_grp[5]
    elif item == 'Bouquet':
        active_parent = parent_grp[6]
    elif item == 'Frog':
        active_parent = parent_grp[7]


def run(item):
    global active_parent
    global active_const
    global offset
    selected = cmds.ls(sl=True,long=True) or []
    cmds.addAttr(ln='Constraint', defaultValue=1.0, minValue=0.0, maxValue=1.0)
    cmds.setAttr(selected[0]+".Constraint",channelBox=True)
    cmds.setAttr(selected[0]+".Constraint",k=True)
    cmds.select(active_parent, add=True)
    if active_const == 'Parent':
        constraint = cmds.parentConstraint(selected[0], active_parent, maintainOffset = offset)
    if active_const == 'Point':
        constraint = cmds.pointConstraint(selected[0], active_parent, maintainOffset = offset)
    if active_const == 'Orient':
        constraint = cmds.orientConstraint(selected[0], active_parent, maintainOffset = offset)
    if active_const == 'Scale':
        constraint = cmds.scaleConstraint(selected[0], active_parent, maintainOffset = offset)
    cmds.select(constraint, add=True)
    selected = cmds.ls(sl=True,long=True) or []
    weight = cmds.listAttr(selected[2])[-1]
    control_weight = selected[0]+".Constraint"
    cmds.connectAttr(control_weight, selected[2]+"."+weight)
    cmds.select(selected[0])


class PropConstUI(object):
   def __init__(self, id):
      self.win = cmds.window(id)   
      self.layout = cmds.columnLayout(parent=self.win, width=100, height=100)
      
      cmds.optionMenu(label='Prop', changeCommand=setProp)
      cmds.menuItem(label = 'Kelleth Doll')
      cmds.menuItem(label = 'Kelleth Doll Head')
      cmds.menuItem(label = 'Maggie Doll')
      cmds.menuItem(label = 'Singe Doll')
      cmds.menuItem(label = 'Wand')
      cmds.menuItem(label = 'Ring')
      cmds.menuItem(label = 'Ring Box')
      cmds.menuItem(label = 'Bouquet')
      cmds.menuItem(label = 'Frog - incomplete')
      
      cmds.optionMenu(label='Constraint Type', changeCommand=setConst)
      cmds.menuItem(label ='Parent')
      cmds.menuItem(label ='Point')
      cmds.menuItem(label ='Orient')
      cmds.menuItem(label ='Scale')
      
      cmds.checkBox(label = "Maintain Offset", changeCommand=setOffset)
        
      cmds.button(label = "Constrain", command=run)
      cmds.showWindow()



class mayaRun:
    def run(self):
        winID = 'Prop Constraint'
        if cmds.window(winID, exists=True):
            cmds.deleteUI(winID)
        UI = PropConstUI(winID)

