import maya.cmds as mc

currentHotkeySet = mc.hotkeySet(q=True, current=True)

unFamiliarHotkeySet = "unFamiliarHotkeySet"

if not mc.hotkeySet(unFamiliarHotkeySet, q=True, ex=True):
    mc.hotkeySet(unFamiliarHotkeySet, source=currentHotkeySet)
    print("Created unFamiliarHotkeySet")

mc.hotkeySet(unFamiliarHotkeySet, edit=True, current=True)

# Hotkey creation 
mc.nameCommand("patternSelect", ann="Pattern Selection", c="python(\"import pipe.tools.mayaTools.UnDev.patternSelect as pSelect; pSelect.patternSelection()\")")
mc.hotkey(k="Up", sht=True, name="patternSelect")

mc.nameCommand("patternSelectRepeat", ann="Pattern Selection Repeat", c="python(\"import pipe.tools.mayaTools.UnDev.patternSelect as pSelect; pSelect.patternSelectionRepeat()\")")
mc.hotkey(k="Up", sht=True, ctl=True, name="patternSelectRepeat")
