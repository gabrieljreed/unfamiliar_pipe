import hou
import os 

#this class deletes all tex files from the given folder 
#wow, baby's first correctly formatted python class 
#HA

class TexDelete():

    def ConfirmChoice(self,popupMessage,popupTitle):
        userChoice = hou.ui.displayMessage(popupMessage,buttons=("okay","close",),default_choice=0,title=popupTitle)

        if(userChoice == 0):
            return 1
        elif(userChoice == 1):
            return 0
            quit()

    def GetInput(self, popupMessage,popupTitle):
        userInput = hou.ui.readInput(popupMessage,buttons=("okay","close",),default_choice=0,title=popupTitle)

        if (userInput[0] == 1):
            quit()
        return userInput[1]

    def GetAssetName(self):
        BASE_PATH = "/groups/unfamiliar/anim_pipeline/production/assets/"
        MAT_PATH = "/materials/textures/RMAN"

        #get selected nodes
        #print("sel nodes = "+str(hou.selectedNodes()))
        if(hou.selectedNodes() == ()):
            print("Please select a node. Closing tool")
            quit()
        matLibNode = hou.selectedNodes()[0]
        #print("matLibNode = " + str(matLibNode))

        #if it's not a material library, yell at them 
        if(matLibNode.type().name() != 'materiallibrary'):
            print("please select a material library node.")
            quit()

        #if it is a material library, grab the asset name 
        if(matLibNode.type().name() == 'materiallibrary'):
            matLibName = str(matLibNode)
            assetName = matLibName.replace("pxr_","")

        #create the path from the base and the asset name 
        assetPath = BASE_PATH + assetName + MAT_PATH

        return(assetName, assetPath)

    def ClearTex(self,PATH,assetName):
        texFilesCleared = 0
        #WAIT ARE YOU REALLY SURE
        self.ConfirmChoice("About to delete tex files for " + assetName + ". Are you sure?","Clearing tex files")
        counter = 0
        for file in os.listdir(PATH):
            if file.endswith(".tex"):
                #okay here we go
                os.remove(PATH + "/" + file)
                texFilesCleared = 1
                counter+=1
        print("Deleted " + str(counter) + " tex files for " + assetName + ".")
        hou.ui.displayMessage("Deleted " + str(counter) + " tex files for " + assetName + ".",buttons=("Okay",),title="Success!")

        if(texFilesCleared == 0):
            print("No tex files found to delete. Closing tool.")
            hou.ui.displayMessage("No tex files found to delete. Closing "+
            "tool.",buttons=("Okay",),title="Error")