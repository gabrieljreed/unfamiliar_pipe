import maya.cmds as mc
import maya.mel as mel
import os, shutil
import pipe.pipeHandlers.environment as environment
import logging

def logMessage(logName, message):
    logger = logging.getLogger(logName)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # prevent logging from bubbling up to maya's logger
    logger.propagate=0
    # 'application' code
    logger.info(message)

def importLayout():
	env = environment.Environment()
	filePath = mc.file(q=True, sn=True)
	curDir = env.get_file_dir(filePath)[1:]
	shotName = curDir.split('/')[-1]
	layoutFilePath = curDir + '/layout/' + shotName + '_layout_main.usda'
	if (len(filePath) == 0):
		logMessage('Layout Import', 'Please save your file to disc before importing the layout')
		return
	elif (filePath.find('/groups/unfamiliar/anim_pipeline/production/anim_shots') == -1):
		layoutDir = curDir + '/layout'
		mayaDefaultLayoutDir = '/groups/unfamiliar/anim_pipeline/production/layout/maya_default_layout.usda'
		layoutFilePath = layoutDir + '/' + filePath.split('/')[-1].split('.')[0] + '_layout_main.usda'
		if os.path.exists(layoutDir) == False:
			os.mkdir(layoutDir)
		shutil.copyfile(mayaDefaultLayoutDir, layoutFilePath)
		logMessage('Layout Import', 'Layout usda file created at ' + layoutFilePath)
	melCommand = 'mayaUsd_createStageFromFilePath ' + '"' + layoutFilePath + '"'
	print(melCommand)
	mel.eval(melCommand)


class mayaRun():
	def run(self):
		importLayout()
