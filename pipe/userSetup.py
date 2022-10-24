"""This script runs on Maya startup and sets up the environment for the pipeline."""

import maya.cmds as mc
import sys

print("Starting unmaya")

# We add the path to the folder containing the custom UnMaya shelves
sys.path.append(r"/groups/unfamiliar/anim_pipeline/pipe/tools/mayaTools/custom")

# Here we use evalDeferred to make sure we don't try to load shelves until after the UI is fully loaded
mc.evalDeferred("import pipe.tools.mayaTools.custom.shelf as shelf")

# Do the same for custom hotkeys
mc.evalDeferred("import pipe.tools.mayaTools.UnDev.setupHotkeys as hotkeys")
