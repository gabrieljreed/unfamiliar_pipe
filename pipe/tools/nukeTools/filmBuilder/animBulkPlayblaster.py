"""Tool to playblast all shots in the anim directory using Maya standalone"""


import os
import sys

import maya.cmds as cmds

sys.path.append(r"/groups/unfamiliar/anim_pipeline/")

import pipe.pipeHandlers.permissions as permissions


editShotsDir = r"/groups/unfamiliar/anim_pipeline/production/edit/shots"
animShotsDir = r"/groups/unfamiliar/anim_pipeline/production/anim_shots"


def playblastAllAnimShots():
    """Utility function to playblast all anim shots"""
    shots = os.listdir(animShotsDir)
    shots.sort()

    skippedShots = []
    for shot in shots:
        mayaFilePath = os.path.join(animShotsDir, shot, shot + "_main.mb")
        if not os.path.isdir(os.path.join(animShotsDir, shot)) or not os.path.exists(mayaFilePath):
            print(f"Skipping {shot} because it's not a shot directory or it doesn't have a main file")
            skippedShots.append(shot)
            continue

        if len(os.listdir(os.path.join(animShotsDir, shot))) == 0:
            continue

        print(f"Playblasting {shot} from {mayaFilePath}")
        # _playblastAnimShot(shot, mayaFilePath)

    print(f"Skipped {len(skippedShots)}/{len(shots)} shots")


def _playblastAnimShot(shot, path):
    """Playblasts a given shot"""
    cmds.file(path, o=True)
    fileName = os.path.join(editShotsDir, "02_anim_playblast", shot, shot)

    width = 1998
    height = 1080
    videoScalePct = 100
    videoCompression = "Animation"
    videoFormat = "qt"

    cmds.lookThru(f"{shot}:ShotCam_000")

    try:
        cmds.playblast(f=fileName, forceOverwrite=True, viewer=False, percent=videoScalePct,
                       format=videoFormat, compression=videoCompression,
                       widthHeight=[width, height])

        # Set permissions
        permissions.set_permissions(f"{fileName}.mov")

    except Exception as e:
        print(f"Error playblasting shot {shot}: {e}")
        return

    # Close the file
    cmds.file(new=True, force=True)


def initializeStandalone():
    try:
        import maya.standalone

        maya.standalone.initialize()
    except Exception:
        pass


def uninitializeStandalone():
    import maya.standalone

    try:
        maya.standalone.uninitialize()
    except Exception as e:
        print("Error uninitializing standalone: {}".format(e))


if __name__ == "__main__":
    initializeStandalone()
    # playblastAllAnimShots()
    # print("loading plugin")
    # cmds.loadplugin("/usr/autodesk/maya2023/plug-ins/fbx/plug-ins/fbxmaya.so")
    # print("plugin loaded")
    # _playblastanimshot("a_020", r"/groups/unfamiliar/anim_pipeline/production/anim_shots/a_020/a_020_main.mb")
    print(cmds.pluginInfo(query=True, listPlugins=True))
    uninitializeStandalone()
