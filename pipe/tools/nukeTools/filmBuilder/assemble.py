import os
import sys
import nuke

appendNode = nuke.createNode("AppendClip")
output = sys.argv[1]

for i, arg in enumerate(sys.argv[2:]):
    if arg.endswith("assemble.py"):
        continue
    print(arg)
    r = nuke.createNode("Read")
    r["file"].setValue(arg)

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

nuke.scriptSave(os.path.dirname(__file__) + "/sequence.nk")
print(f"Saved script to {os.path.dirname(__file__)}")
