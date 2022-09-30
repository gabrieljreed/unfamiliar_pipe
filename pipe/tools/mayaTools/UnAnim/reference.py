import maya.cmds as mc
import logging
import pipe.pipeHandlers.environment as environment
import os

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

class reference:

    def ref(self, filePath, namespace):
        mc.file(filePath, r = True, namespace = namespace)

    def rig(self, rigName):
        if rigName == 'kelleth':
            filePath = '/groups/unfamiliar/anim_pipeline/production/rigs/kelleth/kelleth_main.mb'

        elif rigName == 'maggie':
            filePath = '/groups/unfamiliar/anim_pipeline/production/rigs/maggie/maggie_main.mb'

        elif rigName == 'singe':
            filePath = '/groups/unfamiliar/anim_pipeline/production/rigs/singe/singe_main.mb'

        elif rigName == 'frog':
            filePath = '/groups/unfamiliar/anim_pipeline/production/rigs/frog/frog_main.mb'
        
        elif rigName == 'dolls':
            filePath = '/groups/unfamiliar/anim_pipeline/production/rigs/dolls/dolls_main.mb'

        elif rigName == 'amoogus':
            filePath = '/groups/unfamiliar/anim_pipeline/production/rigs/amoogus/amoogus_main.ma'

        else:
            logMessage('Rig Importer', 'Rig does\'nt exist')
            return
        
        self.ref(filePath, rigName)

    def camera(self):
        env = environment.Environment()
        filePath = mc.file(q=True, sn=True)
        curDir = env.get_file_dir(filePath)[1:]
        if (filePath.find('/groups/unfamiliar/anim_pipeline/production/anim_shots') == -1):
            logMessage('Camera Importer', 'Not in a valid shot file. Please check out a shot and try again.')
            return
        shotName = curDir.split('/')[-1]
        shotsDir = '/groups/unfamiliar/anim_pipeline/production/shots'
        camPath = shotsDir + '/' + shotName + '/camera/camera_main.fbx'
        if os.path.exists(camPath) == False:
            logMessage('Camera Importer', 'No camera has been published for this shot.')
            return
        self.ref(camPath, shotName)
