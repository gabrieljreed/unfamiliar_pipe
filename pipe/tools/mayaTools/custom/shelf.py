import sys
import os 

import create_shelf
from create_shelf import load_shelf

sys.path.append(os.path.dirname(__file__))

# TODO: Grab all [a-z]_shelf.json files in the current directory and load them
load_shelf("UnPrevis", "previs_shelf.json")
load_shelf("UnAnim", "animation_shelf.json")
load_shelf("UnFiles", "shot_management_shelf.json")

print("Successfully loaded shelves!")
