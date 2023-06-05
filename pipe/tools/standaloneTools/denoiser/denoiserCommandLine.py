"""CLI for the denoiser."""

from __future__ import print_function, unicode_literals

import subprocess
import sys
import os

sys.path.append(r"/groups/unfamiliar/anim_pipeline/")
import pipe.tools.standaloneTools.denoiser.denoise as denoise

try:
    from PyInquirer import prompt, print_json, Separator
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInquirer"])
    from PyInquirer import prompt, print_json, Separator

from pprint import pprint


shotsDir = r"/groups/unfamiliar/anim_pipeline/production/shots"
sequences = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]


def getShots(answers):
    """Get the shots for the given sequence."""
    sequence = answers["sequence"]
    shots = os.listdir(shotsDir)
    shots = [shot for shot in shots if shot.startswith(sequence)]
    shots.sort()
    return shots


def getRenderLayers(answers):
    """Get the render layers for the given shot."""
    shot = answers["shot"]
    renderDir = os.path.join(shotsDir, shot, "render")
    layers = os.listdir(renderDir)
    layers.sort()
    layers = [{"name": layer} for layer in layers]
    return layers


questions = [
    {
        'type': 'list',
        'message': 'Select sequence',
        'name': 'sequence',
        'choices': sequences,
    },
    {
        'type': 'list',
        'message': 'Select shot',
        'name': 'shot',
        'choices': getShots,
    },
    {
        'type': 'checkbox',
        'message': 'Select layers',
        'name': 'layers',
        'choices': getRenderLayers,
    },
    {
        'type': 'input',
        'message': 'Blend factor',
        'name': 'blendFactor',
        "default": "0.85",
    },
    {
        'type': 'list',
        'message': 'Select render type',
        'name': 'renderType',
        'choices': [
            'Update denoised (keep undenoised folders, overwrite denoised)',
            'New render (delete undenoised folders, move current to undenoised)',
        ],
    },
]

if __name__ == "__main__":
    answers = prompt(questions)
    # pprint(answers)

    folderPaths = []
    for layer in answers["layers"]:
        folderPath = os.path.join(shotsDir, answers["shot"], "render", layer)
        folderPaths.append(folderPath)

    blendFactor = float(answers["blendFactor"])
    newRender = answers["renderType"].startswith("New render")

    denoise.denoiseFolders(folderPaths, blendFactor, newRender)
