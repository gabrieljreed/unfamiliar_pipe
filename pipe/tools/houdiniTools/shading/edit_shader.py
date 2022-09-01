import hou
import pipe.pipeHandlers.gui as gui
from pipe.pipeHandlers.environment import Environment as env

#This class makes a gui for decided which shader to edit as well as making the 
#correct editing LOP node network
class EditShader():

    def __init__(self):
        #Get asset list
        self.ASSET_PATH = env().get_asset_dir()
        self.asset_list = env().get_asset_list()
        
        
    #This Function lets you manually build the shader network by passing paramters rather than
    #using the gui in the houdini tool
    def manual_call(self, assetname, assettype):
        self.ASSET_TYPE = assettype
        self.ASSET_NAME = assetname
        self.createNodeNetwork()

    #Function called by the "Edit Shader" button in houdini
    def assetSelect(self):
        #Get asset name and type
        self.itemSelectGui()
        

    #Starts the gui for choosing asset
    def itemSelectGui(self):
        #Intilize gui with the asset list
        self.item_gui = gui.SelectFromList(l=self.asset_list, parent=hou.ui.mainQtWindow(), title="Select an asset to shade")
        #Send results from gui to the results method
        self.item_gui.submitted.connect(self.results)


    #Is called after the user interacts with the gui
    def results(self, value):
        self.ASSET_NAME = value[0]
        #Get asset type
        if(self.assetType()):
            #Create the node network
            self.createNodeNetwork()
        
    
    #Gets asset type from user input
    def assetType(self):
        self.ASSET_TYPE = hou.ui.readInput("Input \'previs\' or \'prod\'")[1]
        if (self.ASSET_TYPE != 'previs'):
            if (self.ASSET_TYPE != 'prod'):
                hou.ui.displayMessage("Invaild asset type. Please try again")
                print(self.ASSET_TYPE)
                return False
        return True
        
        
    def createNodeNetwork(self):
        ASSET_TYPE = self.ASSET_TYPE
        ASSET_NAME = self.ASSET_NAME
        ASSET_PATH = self.ASSET_PATH + '/'

        if (ASSET_TYPE == "previs"):
            SHADER_TYPE = "unreal"
        elif (ASSET_TYPE == "prod"):
            SHADER_TYPE = "pxr"

        stage = hou.node("/stage")
            
        #Set up shader network for editing
        assetSubLayer = stage.createNode("sublayer")
        assetSubLayer.parm("filepath1").set(ASSET_PATH + ASSET_NAME + "/" + ASSET_NAME + ".usda")

        editMat = stage.createNode("editmaterial")
        editMat.setInput(0, assetSubLayer, 0)
        editMat.parm("matpath1").set("/" + ASSET_NAME + "/materials/" + SHADER_TYPE + "_" + ASSET_NAME)
        editMat.parm("load1").pressButton()

        matNodeList = editMat.allSubChildren()

        matLib = stage.createNode("materiallibrary", node_name = SHADER_TYPE + "_" + ASSET_NAME)
        matLib.parm("matnode1").set("collect1")
        matLib.parm("matpath1").set(SHADER_TYPE + "_" + ASSET_NAME)
        hou.copyNodesTo(matNodeList, matLib)

        assetSubLayer.destroy()
        editMat.destroy()

        #Set up asset viewer subnet
        objectViewer = stage.createNode("subnet", node_name = "OBJECT_VIEWER")
        objectViewer.setInput(0, matLib, 0)
        objectViewer.setDisplayFlag(True)

        configLayer = objectViewer.createNode("configurelayer")
        configLayer.parm("setsavepath").set(True)
        configLayer.parm("savepath").set(ASSET_PATH + ASSET_NAME + "/materials/" + SHADER_TYPE + "_" + ASSET_NAME + ".usda")
        configLayer.setInput(0, objectViewer.indirectInputs()[0], 0)

        geo = objectViewer.createNode("sublayer", node_name = ASSET_TYPE + "_" + ASSET_NAME)
        geo.parm("filepath1").set(ASSET_PATH + ASSET_NAME + "/geo/" + ASSET_TYPE + "_" + ASSET_NAME + ".usd")

        transform = objectViewer.createNode("xform", node_name = "fix_scale")
        transform.parm("scale").set(0.01)
        transform.setInput(0, geo, 0)

        ref = objectViewer.createNode("reference", node_name = "materials")
        ref.parm("reftype").set("inputref")
        ref.setInput(0, transform, 0)
        ref.setInput(4, configLayer, 0)

        assignMat = objectViewer.createNode("assignmaterial")
        assignMat.parm("primpattern1").set("/Geometry")
        assignMat.parm("matspecpath1").set("/materials/" + SHADER_TYPE + "_" + ASSET_NAME)
        assignMat.setInput(0, ref, 0)

        output = hou.node(objectViewer.path() + "/output0")
        output.setInput(0, assignMat, 0)
        output.setDisplayFlag(True)

        #Set up usd rop for export
        usdRop = stage.createNode("usd_rop", node_name = "EXPORT_SHADER")
        usdRop.setInput(0, objectViewer, 0)
        usdRop.parm("lopoutput").set("/groups/unfamiliar/shading/throwaway_usd/" + ASSET_NAME + "_delete.usda")

        ### This is a patch to 1. correct the filepath on pxrtextures when loading a previosuly 
        #created shader 2. activate a couple important parameters. Eventually I want to activate
        #all parameters by default, but I don't have time for that rn. lmk if this causes bugs.
        # - anna
        '''
        #ZACH EDIT bro we gotta clean up this code later frfr. anyways editing this section out and adding
        #a single line so Anna's patch only affects the currently created matnet, not all of them.
        stageNodes = stage.children()
        print(stageNodes)
        matLibNodes = []
        #get all material library nodes in stage
        for node in stageNodes:
            if(node.name().startswith("pxr") or node.name().startswith("unreal")):
                matLibNodes.append(node)
                print(matLibNodes)
		'''
        matLibNodes = [matLib]
        '''
        #END ZACH EDIT OF ANNA'S EDIT. ugh 
        '''
        #for each material library node... 
        for matLibNode in matLibNodes:
            #get all children
            matLibChildren = matLibNode.children()
            print(matLibChildren)
            #get asset name from material library node name
            assetName = matLibNode.name().replace("pxr_","")

            #FIX PXRTEXTURES
            #determine which are pxrtextures and add to a list
            pxrTexNodes = []
            for node in matLibChildren:
                if("pxrtexture::3.0" in str(node.type())):
                    pxrTexNodes.append(node)
                #and the normal map! 
                elif("pxrnormalmap::3.0" in str(node.type())):
                    pxrTexNodes.append(node)
            #fix each filepath
            for texNode in pxrTexNodes:
                print("fixing a filepath in a pxrtexture")
                #activate filename parameter
                texNode.parm("__activate__filename").set(1)
                #check that filename hasn't already been fixed
                if(texNode.parm("filename").eval().startswith("./textures")):
                    ogFilename = texNode.parm("filename").eval()
                    newFilename = ogFilename.replace("./textures/","$JOB/assets/"+assetName+"/materials/textures/")
                    texNode.parm("filename").set(newFilename)

            #FIX PXRMIXES
            #determine which are pxrmixes and add to a list
            pxrMixNodes = []
            for node in matLibChildren:
                if("pxrmix::3.0" in str(node.type())):
                    pxrMixNodes.append(node)
            #turn on each color parameter
            for mixNode in pxrMixNodes:
                mixNode.parm("__activate__color1").set(1)
                mixNode.parm("__activate__color2").set(2)

            #FIX USDUVTEXTURES
            #determine which are usduvtextures and add to a list
            usdUvNodes = []
            for node in matLibChildren:
                print(node.type())
                if("usduvtexture::2.0" in str(node.type())):
                    usdUvNodes.append(node)
            print(usdUvNodes)
		    
            #fix each filepath
            for uvNode in usdUvNodes:
                print("fixing a usd uv texture node")
                #activate filename parameter
                uvNode.parm("__activate__file").set(1)
                #activate scale and bias(for displacement)
                uvNode.parm("__activate__scale").set(1)
                uvNode.parm("__activate__bias").set(1)
                ogFilePath = uvNode.parm("file").eval()
                FileName = ogFilePath.split('/')[-1]
                newFilePath = "$JOB/assets/"+ASSET_NAME+"/materials/textures/PBRMR/"+FileName
                uvNode.parm("file").set(newFilePath)
            
            #FIX USDPRIMVARREADER
            #determine which is a usdprimvarreader and add to a list
            #yes I know there should only be one and i should write a function for this
            #but I Do Not Have Time
            usdPrimvarReaderNodes = []
            for node in matLibChildren:
                if("usdprimvarreader" in str(node.type())):
                    print("fixing a usd primvar reader")
                    usdPrimvarReaderNodes.append(node)
		    
            #activate parameters
            for node in usdPrimvarReaderNodes:
                #activate filename parameter
                node.parm("__activate__signature").set(1)
                node.parm("__activate__varname").set(1)
        ### end patch ###

        objectViewer.layoutChildren()
        stage.layoutChildren()