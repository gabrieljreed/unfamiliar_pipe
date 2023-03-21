"""Assemble a sequence of frames or videos into a single video file."""


import os
import sys
import nuke
import subprocess


def countFrames(path):
    """Count the number of frames in a video file."""
    s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=nb_read_frames", "-print_format", "csv", path], stdout=subprocess.PIPE)
    result = int(s.stdout.decode().split(",")[1])
    return result


appendNode = nuke.createNode("AppendClip")
output = sys.argv[1]
totalFrames = 0

for i, arg in enumerate(sys.argv[2:]):
    if arg.endswith("assemble.py"):
        continue
    filePath = os.listdir(arg)

    if len(filePath) == 0:
        print(f"Warning: {arg} is empty. Skipping...")
        continue

    print(f"found {len(filePath)} files in {arg}")

    # Get the most recently modified file
    mostRecentTime = os.path.getmtime(os.path.join(arg, filePath[0]))
    finalFilePath = os.path.join(arg, filePath[0])

    for file in filePath:
        if os.path.getmtime(os.path.join(arg, file)) > mostRecentTime:
            finalFilePath = os.path.join(arg, file)
            mostRecentTime = os.path.getmtime(os.path.join(arg, file))

    # finalFilePath = os.path.join(arg, filePath[0])

    print(finalFilePath)

    r = nuke.createNode("Read")
    r["file"].setValue(finalFilePath)
    r["colorspace"].setValue("color_picking")
    numFrames = countFrames(finalFilePath)
    totalFrames += numFrames
    r["last"].setValue(numFrames)
    r["origlast"].setValue(numFrames)
    r["origset"].setValue(True)

    appendNode.setInput(i, r)

# Deselect all nodes
allNodes = nuke.allNodes()
for node in allNodes:
    node.knob("selected").setValue(False)

w = nuke.createNode('Write')
w["file"].setValue(output)
w["file_type"].setValue("mov")
w["mov_prores_codec_profile"].setValue("ProRes 4:4:4:4 XQ 12-bit")
w["create_directories"].setValue(True)
w["colorspace"].setValue("color_picking")
w.setInput(0, appendNode)

currentSequence = os.path.basename(output).split(".")[0]

nuke.root()["last_frame"].setValue(totalFrames)
nuke.scriptSave(os.path.dirname(__file__) + f"/{currentSequence}.nk")
print(f"Saved script to {os.path.dirname(__file__)}")
print(f"Total frames: {totalFrames}")
print(f"Executing...")

try:
    nuke.execute(w, 1, totalFrames)
except Exception as e:
    print(f"Failed to execute {currentSequence}")
    print(e)
    exit()

print(f"Done executing {currentSequence}")
