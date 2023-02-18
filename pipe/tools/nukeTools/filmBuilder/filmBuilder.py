"""Run this script to automatically make a film"""

import os

# import nuke


productionShotsDir = r"/groups/unfamiliar/anim_pipeline/production/shots"
editShotsDir = r"/groups/unfamiliar/anim_pipeline/production/edit/shots"
editSequencesDir = r"/groups/unfamiliar/anim_pipeline/production/edit/sequences"


SEQ_A = "A"
SEQ_B = "B"
SEQ_C = "C"
SEQ_D = "D"
SEQ_E = "E"
SEQ_F = "F"
SEQ_G = "G"
SEQ_H = "H"
SEQ_I = "I"

sequences = [SEQ_A, SEQ_B, SEQ_C, SEQ_D, SEQ_E, SEQ_F, SEQ_G, SEQ_H, SEQ_I]

PREVIS = "01_previs"
ANIM_PLAYBLAST = "02_anim_playblast"
FX_PLAYBLAST = "03_fx_playblast"
LIGHTING_BEAUTY = "04_lighting_beauty"
TEMP_MP4 = "05_temp_mp4"

allVersionDirs = [PREVIS, ANIM_PLAYBLAST, FX_PLAYBLAST, LIGHTING_BEAUTY, TEMP_MP4]


def buildFilm():
    """Builds the film"""
    for sequence in sequences:
        buildSequence(sequence)

    sequenceString = ""
    for file in os.listdir(editSequencesDir):
        if file.endswith(".mov"):
            sequenceString += os.path.join(editSequencesDir, file) + " "

    command = """
export MEDIA_PROJECT_DIR=/groups/unfamiliar/anim_pipeline
export MEDIA_PIPE_DIR=$MEDIA_PROJECT_DIR/pipe
#Environment variable for location of python scripts
export PYTHONPATH=${MEDIA_PROJECT_DIR}:${MEDIA_PIPE_DIR}:${MEDIA_PROJECT_DIR}/lib/
unset OCIO

export NUKE_PATH=${MEDIA_PROJECT_DIR}/pipe:${MEDIA_PROJECT_DIR}/pipe/tools/nukeTools:${MEDIA_PROJECT_DIR}/lib/NukeSurvivalToolkit

        """

    pythonFile = os.path.normpath(os.path.join(os.path.dirname(__file__), "assemble.py"))

    output = os.path.join(editSequencesDir, "film.mov")
    lastLine = f"/opt/Nuke13.2v2/Nuke13.2 -t {pythonFile} {output} {sequenceString}"
    command += "\n" + lastLine

    print(command)
    os.system(command)


def buildSequence(sequence):
    """Builds the given sequence"""
    sequenceShots = [shot for shot in os.listdir(productionShotsDir) if shot.startswith(sequence)]
    sequenceShots.sort()
    print(f"Building sequence {sequence}...")
    shotDirs = []
    shotDirsString = ""
    for shot in sequenceShots:
        print(f"\tBuilding shot {shot}...")
        mostRecentVersion = getMostRecentShotVersion(shot)
        print(f"\t\tMost recent version is {mostRecentVersion}")
        shotDirs.append(os.path.join(editShotsDir, mostRecentVersion, shot))
        shotDirsString += os.path.join(editShotsDir, mostRecentVersion, shot) + " "

    command = """
export MEDIA_PROJECT_DIR=/groups/unfamiliar/anim_pipeline
export MEDIA_PIPE_DIR=$MEDIA_PROJECT_DIR/pipe
#Environment variable for location of python scripts
export PYTHONPATH=${MEDIA_PROJECT_DIR}:${MEDIA_PIPE_DIR}:${MEDIA_PROJECT_DIR}/lib/
unset OCIO

export NUKE_PATH=${MEDIA_PROJECT_DIR}/pipe:${MEDIA_PROJECT_DIR}/pipe/tools/nukeTools:${MEDIA_PROJECT_DIR}/lib/NukeSurvivalToolkit

        """

    pythonFile = os.path.normpath(os.path.join(os.path.dirname(__file__), "assemble.py"))

    output = editSequencesDir + f"/SEQ_{sequence}.mov"

    lastLine = f"/opt/Nuke13.2v2/Nuke13.2 -t {pythonFile} {output} {shotDirsString}"
    command += "\n" + lastLine

    print(command)
    os.system(command)


def getMostRecentShotVersion(shotName, includeTempMp4=False):
    """Returns the most recent version of the shot specified by shotName"""

    # versionsDirs = os.listdir(editShotsDir)
    # versionsDirs.sort()

    # if includeTempMp4:
    #     versionsDirs = versionsDirs[0:5]
    # else:
    #     versionsDirs = versionsDirs[0:4]

    versionsDirs = ["02_anim_playblast", "03_fx_playblast", "04_lighting_beauty", "05_temp_mp4"]
    if not includeTempMp4:
        versionsDirs = versionsDirs[0:3]

    mostRecentTime = os.path.getmtime(os.path.join(editShotsDir, versionsDirs[0], shotName))
    mostRecentVersion = versionsDirs[0]

    for versionDir in versionsDirs:
        # Uncomment this when we're actually ready to go
        # if len(os.listdir(os.path.join(editShotsDir, versionDir, shotName))) == 0:
        #     continue

        shotDir = os.path.join(editShotsDir, versionDir, shotName)
        modifiedTime = os.path.getmtime(shotDir)
        if modifiedTime > mostRecentTime:
            mostRecentTime = modifiedTime
            mostRecentVersion = versionDir

    return mostRecentVersion


def _checkShots(versionDir, checkMissing=True):
    """Utility function to check for missing shots"""
    versionDir = os.path.join(editShotsDir, versionDir)
    shots = os.listdir(versionDir)
    shots.sort()
    if checkMissing:
        missingShots = 0
        for shot in shots:
            if not os.path.isdir(os.path.join(versionDir, shot)):
                continue

            if len(os.listdir(os.path.join(versionDir, shot))) == 0:
                print(f"Missing shot: {shot}")
                missingShots += 1

        print(f"Missing {missingShots}/{len(shots)} shots")

    else:
        foundShots = 0
        for shot in shots:
            if not os.path.isdir(os.path.join(versionDir, shot)):
                continue

            if len(os.listdir(os.path.join(versionDir, shot))) != 0:
                print(f"Shot {shot} has files")
                foundShots += 1

        print(f"Found {foundShots}/{len(shots)} shots")


if __name__ == "__main__":
    # print(getMostRecentShotVersion("A_010"))
    # buildSequence(SEQ_A)
    _checkShots(FX_PLAYBLAST, checkMissing=False)
