import nuke
import os

currentFilePath = nuke.scriptName()
exportPath = ""

firstFrame = nuke.frange.minFrame()
lastFrame = nuke.frange.maxFrame()

writeFinal = nuke.nodes.Write(file=exportPath, file_type="exr", write_ACES_compliant_EXR=True)

for i in range(writeFinal.getNumKnobs()):
    print(writeFinal.knob(i).name())


# nuke.execute(writeFinal, firstFrame, lastFrame, 1)
