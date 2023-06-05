"""Contains functions for denoising a given image."""

import copy
import json
import os
import shutil
import subprocess
import sys
import threading

try:
    from tqdm import tqdm
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm

sys.path.append(r"/groups/unfamiliar/anim_pipeline")

import pipe.pipeHandlers.permissions as permissions
import pipe.tools.pythonTools.stringUtilities as stringUtilities


jsonSettingsFilePath = "/groups/unfamiliar/anim_pipeline/pipe/tools/houdiniTools/render/render_settings.json"


def denoiseFolders(folderPaths, blendFactor=0.85, newRender=False):
    """Denoise all images in the given folders.

    Arguments:
        folderPaths {list} -- List of paths to the folders containing the images to denoise.
        blendFactor {float} -- Blend factor for OIDN denoiser. (default: 0.85)
        newRender {bool} -- If True, any "undenoised" folders will be deleted. (default: False)
    """
    if newRender:
        foldersToDelete = []
        totalFoldersToDelete = 0
        totalFilesToDelete = 0
        for item in folderPaths:
            undenoisedFolderPath = os.path.join(item, "undenoised")
            if not os.path.isdir(undenoisedFolderPath):
                print(f"No undenoised folder found in {item} to delete. Skipping...")
                continue

            foldersToDelete.append(undenoisedFolderPath)
            totalFoldersToDelete += 1
            totalFilesToDelete += len(os.listdir(undenoisedFolderPath))

        if totalFoldersToDelete > 0:
            for folder in foldersToDelete:
                shutil.rmtree(folder)
                print(f"Deleted {folder}")

    for folder in folderPaths:
        thread = threading.Thread(target=denoiseFolder, args=(folder, blendFactor))
        thread.start()


def denoiseFolder(folderPath, blendFactor=0.85):
    """Denoise all images in the given folder.

    Arguments:
        folderPath {str} -- Path to the folder containing the images to denoise.
        blendFactor {float} -- Blend factor for OIDN denoiser. (default: 0.85)
    """
    images = os.listdir(folderPath)
    images.sort()

    aovs = getAOVs()

    if not os.path.exists(os.path.join(folderPath, "undenoised")):
        os.makedirs(os.path.join(folderPath, "undenoised"))

        for f in images:
            if not os.path.isfile(os.path.join(folderPath, f)):
                continue

            shutil.move(os.path.join(folderPath, f), os.path.join(folderPath, "undenoised", f))

    images = os.listdir(os.path.join(folderPath, "undenoised"))

    errors = []

    # for i, img in enumerate(images):
    for img in tqdm(images, desc=os.path.basename(folderPath)):
        blendFactorCommand = '\'{"blendfactor":' + str(blendFactor) + '}\''

        inPath = os.path.join(folderPath, "undenoised", img)
        outPath = os.path.abspath(os.path.join(folderPath, img))
        command = f"idenoise {inPath} {outPath} -d oidn -n nn -a albedo --options {blendFactorCommand} --aovs {aovs}"

        result = subprocess.run(
            command, cwd=folderPath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        stdout = result.stdout
        if stdout is not None:
            # print(f"stdout: {stdout}")
            if not isinstance(stdout, str):
                stdout = stdout.decode("utf-8")
                # print(f"decoded stdout: {stdout}")

            while len(stdout) > 0:
                aov = stringUtilities.stripPrefix(stdout, "Error: failed to apply denoiser on ")
                aov = aov.split(" ")[0]
                aov = stringUtilities.stripSuffix(aov, ",")
                aovsCopy = aovs.split(" ")
                aovsCopy.remove(aov)
                aovsCopy = " ".join(aovsCopy)
                newCommand = f"idenoise {inPath} {outPath} -d oidn -n nn -a albedo --options {blendFactorCommand} --aovs {aovsCopy}"
                result = subprocess.run(
                    newCommand, cwd=folderPath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout = result.stdout

                # errors.append(f"{img}: {stdout}")

    permissions.set_permissions(folderPath)
    print(f"Finished denoising {os.path.basename(folderPath)}. ({len(images)} images denoised)")
    # if len(errors) > 0:
    #     print(f"{len(errors)} Errors:")
    #     for error in errors:
    #         print(error)


def getAOVs():
    """Get the AOVs from the render settings."""
    jsonFile = json.load(open(jsonSettingsFilePath, "r"))
    aovs = ""
    for aov in jsonFile["AOVs"]:
        if aov == "u" or aov == "v":
            continue

        aovs += aov + " "

    return aovs
