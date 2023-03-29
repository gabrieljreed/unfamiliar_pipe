"""Export a given shot to a temp mp4 file."""


import os
import sys
import nuke


productionShotsDir = r"/groups/unfamiliar/anim_pipeline/production/shots"
tempMp4Dir = r"/groups/unfamiliar/anim_pipeline/production/edit/shots/05_temp_mp4"


shotName = sys.argv[1]

nukeScriptPath = os.path.join(productionShotsDir, shotName, "nuke", f"{shotName}_main.nk")
outputPath = os.path.join(tempMp4Dir, shotName, f"{shotName}.mov")

# Load the nuke script
nuke.scriptOpen(nukeScriptPath)

# Search all nodes in the script for a write node
writeNode = None
for node in nuke.allNodes():
    if not node.Class() == "Write":
        continue
    if "temp_mp4" not in node["file"].value():
        continue
    writeNode = node
    break

if not writeNode:
    raise Exception("No write node found.")

try:
    nuke.execute(writeNode, 1, int(nuke.root()["last_frame"].value()))
except Exception as e:
    print(f"Failed to export temp mp4 for {shotName}.")
    print(e)
    raise Exception("Failed to export temp mp4.")

print(f"Exported temp mp4 for {shotName} to {outputPath}")
