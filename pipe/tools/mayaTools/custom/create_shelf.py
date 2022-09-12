'''
	Welcome to the Maya shelf script!

	If you'd like to add a shelf button, you can add it to
	the json file for that shelf. Follow the example of the
	other buttons in json shelf files.
	Remember, the icon should be a .svg and the function
	must be implemented in the specified tool location
'''
import pymel.core as pm
import os
import sys
import json
import pipe.tools.mayaTools.UnDev.unloadPackages as unload


SHELF_DIR = os.environ.get('MAYA_SHELF_DIR')
ICON_DIR = os.environ.get('MAYA_ICONS_DIR')
print("SHELF_DIR: {}".format(SHELF_DIR))
os.environ["DCC_ASSET_NAME"] = ""
os.environ["DCC_DEPARTMENT"] = ""

'''
	Shelf building code. You shouldn't have to edit anything
	below these lines. If you want to add a new shelf item,
	follow the instructions at the top of this file.
'''
def load_shelf(shelfName, fileName):
	# Doing this again as a safety measure for when loading shelves using python
	SHELF_DIR = os.environ.get('MAYA_SHELF_DIR')
	ICON_DIR = os.environ.get('MAYA_ICONS_DIR')

	# Load in the json data
	json_file = open(os.path.join(SHELF_DIR, fileName))
	data = json.loads(json_file.read())

	if "shelfName" in data:
		shelfName = data["shelfName"]
	else:
		shelfName = os.path.splitext(fileName)[0]

	print("Loading shelf: {}".format(shelfName))
	delete_shelf(shelfName)
	deleteSimilarShelves(os.path.splitext(fileName)[0])
	unload.unloadPackages(silent=True)  # I don't think you really need this because Maya is starting up, but it doesn't hurt 


	gShelfTopLevel = pm.mel.eval('global string $gShelfTopLevel; string $temp=$gShelfTopLevel')
	pm.shelfLayout(shelfName, cellWidth=33, cellHeight=33, p=gShelfTopLevel)
	
	for shelf_item in data['shelfItems']:
		if shelf_item['itemType'] == 'button':
			icon = os.path.join(ICON_DIR, shelf_item['icon'])
			annotation = shelf_item['annotation']
			label = shelf_item['label']

			# dcc = double click command: we can add a different command that goes when double clicked.
			dcc = shelf_item['double-click']
			# menu = submenu for right-click
			menu = shelf_item['menu']

			path = "pipe.tools." + shelf_item['tool']
			function = shelf_item['function']
			class_with_method = function.split(".")
			module = class_with_method[0]
			method = class_with_method[1]

			command_base = "from " + str(path) + " import " + str(module) + "; shelf_item = " + str(module) + "(); shelf_item."
			command = command_base + str(method)

			if dcc == 0:
				dcc = command
			else:
				dcc = command_base + str(dcc)

			if menu == 0:
				pm.shelfButton(c=command, ann=annotation, i=icon, l=annotation, iol=label, olb=(0,0,0,0), dcc=dcc)
			elif menu == 1:
				menu_items = shelf_item['menu_items']
				new_menu = build_menu_string(command_base, menu_items)
				mip = []
				for i in range (len(new_menu)):
					mip.append(i)
				pm.shelfButton(c=command, ann=annotation, i=icon, l=annotation, iol=label, olb=(0,0,0,0), dcc=dcc, mi=new_menu, mip=mip)

		else:
			pm.separator(horizontal=False, style='shelf', enable=True, width=35, height=35, visible=1, enableBackground=0, backgroundColor=(0.2,0.2,0.2), highlightColor=(0.321569, 0.521569, 0.65098))

	# Set default preferences
	pm.env.optionVars['generateUVTilePreviewsOnSceneLoad'] = 1

	# shelf loaded correctly
	print("*** Shelf loaded :) ***")
	sys.path.append(os.getcwd())

def build_menu_string(command_base, menu_items):
	menu = []
	menu_python = [0,1,2,3]
	for item in menu_items.items():
		menu_command = command_base + str(item[1])
		label = item[0]
		new_item = [label, menu_command]
		menu.append(new_item)

	return menu

def delete_shelf(shelfName):
	if pm.shelfLayout(shelfName, exists=True):
		pm.deleteUI(shelfName)


def deleteSimilarShelves(fileName):
	"""Deletes all shelves that have the same name as the file name
	@param fileName: The name of the shelf file"""
	mayaPath = os.path.join(os.environ['MAYA_APP_DIR'], '2023', 'prefs', 'shelves')

	for file in os.listdir(mayaPath):
		if fileName in file or "json" in file:
			os.remove(os.path.join(mayaPath, file))
			print("Deleted old shelf: {}".format(file))
