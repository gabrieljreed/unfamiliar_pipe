from ast import If
from cgi import test
from email.mime import base
from socket import TCP_NODELAY
import hou 
import os 
import pathlib
from pipe.pipeHandlers.environment import Environment as env

#This class gets the name of an asset from a selected material library node, 
#then builds a basic shading network based on that information. 

class BuildShader():

    def __init__(self,purpose="prod",prefix="pxr_",identifier="DiffuseColor",
        UDIMs=False,fileFormat=".png",filePath="no filepath",shaderName="no shader name"):
        self.purpose = purpose
        self.prefix = prefix
        self.identifier = identifier

        self.UDIMs = UDIMs
        self.fileFormat = fileFormat
        self.filePath = filePath
        self.shaderName = shaderName

    def get_purpose(self):
        return self.purpose
    
    def set_purpose(self,purpose):
        self.purpose = purpose
        if(purpose == "prod"):
            self.prefix = "pxr_"
            self.identifier = "DiffuseColor"
        elif(purpose == "previs"):
            self.prefix = "unreal_"
            self.identifier = "BaseColor"

    def get_UDIMs(self):
        return self.UDIMs

    def set_UDIMs(self, UDIMs):
        self.UDIMs = UDIMs

    def get_fileFormat(self):
        return self.fileFormat

    def set_fileFormat(self, fileFormat):
        self.fileFormat = fileFormat

    def get_filePath(self):
        return self.filePath

    def set_filePath(self,filePath):
        self.filePath = filePath

    def get_shaderName(self):
        return self.shaderName

    def set_shaderName(self,shaderName):
        self.shaderName = shaderName

    def DefineAssetInfo(self):
        #get selected nodes
        #print("sel nodes = "+str(hou.selectedNodes()))
        if(hou.selectedNodes() == ()):
            print("Please select a material library node. Closing tool.")
            hou.ui.displayMessage("Please select a material library "+
            "node.",buttons=("Okay",),title="Error")
            quit()
        matLibNode = hou.selectedNodes()[0]
        #print("matLibNode = " + str(matLibNode))

        #if it's not a material library, yell at them 
        if(matLibNode.type().name() != 'materiallibrary'):
            print("Please select a material library node. Closing tool.")
            hou.ui.displayMessage("Please select a material library "+
            "node.",buttons=("Okay",),title="Error")
            quit()

        #if it is a material library, determine the purpose
        if(str(matLibNode).startswith("pxr_")):
            self.set_purpose("prod")
        elif(str(matLibNode).startswith("unreal_")):
            self.set_purpose("previs")

        #and grab the asset name 
        if(matLibNode.type().name() == 'materiallibrary'):
            matLibName = str(matLibNode)
            print("self.prefix = "+str(self.prefix))
            assetName = matLibName.replace(self.prefix,"")
            self.shaderName = assetName
        
        print("shader name is "+str(self.shaderName))

        #define paths
        BASE_PATH = "/groups/unfamiliar/anim_pipeline/production/assets/"
        if(self.purpose=="prod"):
            MAT_PATH = "/materials/textures/RMAN"
        elif(self.purpose=="previs"):
            MAT_PATH = "/materials/textures/PBRMR"

        #create the path from the base and the asset name 
        self.filePath = BASE_PATH + self.shaderName + MAT_PATH
        
        '''
        #prod or previs?
        if(self.shaderName.startswith("pxr_")):
            self.set_purpose("prod")
        elif(self.shaderName.startswith("unreal_")):
            self.set_purpose("previs")
        '''

        #access first file in folder to determine file format and if it uses udims 
        testFile = os.listdir(self.filePath)[0]

        #file format?
        if(".png" in str(testFile)):
            self.fileFormat = ".png"
        elif(".exr" in str(testFile)):
            self.fileFormat = ".exr"
        elif(".jpg" in str(testFile)):
            self.fileFormat = ".jpg"
        elif(".tif" in str(testFile)):
            self.fileFormat = ".tif"

        #UDIMs?
        if(".1" in str(testFile)):
            self.UDIMs = True
        else: self.UDIMs = False

    def ImportTextureFile(self,mapTypeNode,mapTypeString):
        importedMap = 0
        folder = os.listdir(self.filePath)
        for file in folder:
            if(file.startswith(self.shaderName) and (mapTypeString in file) and file.endswith(self.fileFormat) and importedMap == 0):
                #print ("importing the following file: " + str(file))
                fullFilePath = self.filePath + "/" + str(file)
                #print ("unmodified full file path is as follows: " + fullFilePath)
                if(self.UDIMs == 1):
                    #SET FILE PATH USING UDIM SYNTAX
                    #remove ".10**.fileformat" and replace with ".<UDIM>.fileformat"
                    splitIndex = fullFilePath.find(".10")
                    udimFilePath = fullFilePath[:splitIndex] + ".<UDIM>"+self.fileFormat
                    #set file path to correct UDIM syntax
                    if(self.purpose == "prod"):
                        mapTypeNode.parm("filename").set(udimFilePath)
                    elif(self.purpose == "previs"):
                        mapTypeNode.parm("file").set(udimFilePath)
                    #print ("UDIM file path is as follows: " + udimFilePath)
                elif(self.UDIMs == 0):
                    #print("no UDIMs")
                    #SET FILE PATH DEFAULT METHOD
                    if(self.purpose == "prod"):
                        mapTypeNode.parm("filename").set(fullFilePath)
                    elif(self.purpose == "previs"):
                        mapTypeNode.parm("file").set(fullFilePath)
                importedMap = 1

    def ShaderBuild(self):
        folder = os.listdir(self.filePath)

        print("building a "+self.purpose+" shader")
        print("Creating shader for \""+self.shaderName+"\". Maps located at \""+self.filePath+"\"")

        matLibLoc = "/stage/"+self.prefix+str(self.shaderName)+"/"
        matLib = hou.node(matLibLoc)
        print("matLibLoc = "+str(matLibLoc))
        print("matLib = "+str(matLib))
        if(matLib == None):
            print("no material library found :(")
        #TODO: if node doesn't exist, create it and use that as a location to build the shader

        #Prep material library 
        allPreviewSurfaces = hou.vopNodeTypeCategory().nodeType("usdpreviewsurface").instances()

        #get only the items we want from the toDelete tuple and store them in a list
        toDelete = []
        for node in allPreviewSurfaces:
            #print("curnode = "+str(node))
            if(self.prefix in str(node)):
                toDelete.append(node)
        #then delete everything in that list 
        if(len(toDelete)!=0):
            i=0
            for node in toDelete:
                #print("deleting "+str(node))
                toDelete[i].destroy()
                i+=1

        #define output collect
        if(hou.node(matLibLoc+"collect1") != None):
            outputCollect = hou.node(matLibLoc+"collect1")
        else: outputCollect = matLib.createNode("collect")

        #Create basic shading network 
        if(self.purpose == "prod"):
            #create pxrSurface and wire into output_collect
            pxrSurface = matLib.createNode("pxrsurface","pxr_"+self.shaderName)
            outputCollect.setInput(0,pxrSurface,0)
            #diffuse color
            diffuseColor = matLib.createNode("pxrtexture","diffuse_color_pxrtexture")
            #diffuseColor.parm("linearize").set(1)
            pxrSurface.setInput(2,diffuseColor,0)
            #specular face color
            specFaceColor = matLib.createNode("pxrtexture","spec_face_color_pxrtexture")
            #specFaceColor.parm("linearize").set("1")
            pxrSurface.setInput(9,specFaceColor,0)
            #specular roughness
            specRoughness = matLib.createNode("pxrtexture","spec_roughness_pxrtexture")
            pxrSurface.setInput(14,specRoughness,1)
            #normal 
            normal = matLib.createNode("pxrnormalmap","normal_map")
            normal.parm("invertBump").set("1")
            #normal.parm("bumpScale").set(0.75)
            pxrSurface.setInput(103,normal,0)
            #presence
            presence = matLib.createNode("pxrtexture","presence_pxrtexture")
            pxrSurface.setInput(105,presence,1)
            #displacement
            pxrDisplace = matLib.createNode("pxrdisplace")
            #note: this is just a starting place. you'll likely have to adjust it manually furthur)
            pxrDisplace.parm("dispAmount").set("0.25")
            outputCollect.setInput(1,pxrDisplace,0)
            pxrDispTransform = matLib.createNode("pxrdisptransform")
            #this is assuming your displacement map has a midpoint of 0.5 
            #(which if you're using substance painter usually it will)
            pxrDispTransform.parm("dispRemapMode").set("2")
            pxrDisplace.setInput(1,pxrDispTransform,1)
            displacement = matLib.createNode("pxrtexture","displacement_pxrtexture")
            pxrDispTransform.setInput(0,displacement,1)

            ###############DELETE LATER###########################3
            remap = matLib.createNode("pxrremap")
            remap.parm("inputMax").set(0.25)
            remap.setInput(0,diffuseColor,0)
            pxrSurface.setInput(2,remap,0)
            #######################################################


            #layout nodes inside material library
            matLib.layoutChildren()

        elif(self.purpose == "previs"):
            #create primvar reader
            usdPrimvarReader = matLib.createNode("usdprimvarreader")
            usdPrimvarReader.parm("signature").set("float2")
            usdPrimvarReader.parm("varname").set("st")
            #create USD Preview Surface and wire into output_collect
            usdPrevSurface = matLib.createNode("usdpreviewsurface","unreal_"+self.shaderName)
            outputCollect.setInput(0,usdPrevSurface,0)
            #base color
            baseColor = matLib.createNode("usduvtexture::2.0","diffuse_color_usduvtexture")
            #############TEMP FIX FOR COLOR SPACE ISSUE####################
            baseColor.parm("scaler").set(3)
            baseColor.parm("scaleg").set(3)
            baseColor.parm("scaleb").set(3)
            baseColor.setInput(1,usdPrimvarReader,0)
            usdPrevSurface.setInput(0,baseColor,4)
            #metallic
            metallic = matLib.createNode("usduvtexture::2.0","metallic_usduvtexture")
            metallic.setInput(1,usdPrimvarReader,0)
            usdPrevSurface.setInput(4,metallic,0)
            #roughness
            roughness = matLib.createNode("usduvtexture::2.0","roughness_usduvtexture")
            roughness.setInput(1,usdPrimvarReader,0)
            usdPrevSurface.setInput(5,roughness,0)
            #normal 
            normal = matLib.createNode("usduvtexture::2.0","normal_usduvtexture")
            normal.setInput(1,usdPrimvarReader,0)
            usdPrevSurface.setInput(10,normal,4)
            #height
            height = matLib.createNode("usduvtexture::2.0","height_usduvtexture")
            height.setInput(1,usdPrimvarReader,0)
            #fix scaling. this is just a starting point.
            height.parm("scaler").set(0.001)
            height.parm("biasr").set(-0.5)
            usdPrevSurface.setInput(11,height,0)
            #layout nodes inside material library
            matLib.layoutChildren()

        #point filepaths to textures 
        if(self.purpose == "prod"):
            self.ImportTextureFile(diffuseColor, "DiffuseColor")
            self.ImportTextureFile(specFaceColor, "SpecularFaceColor")
            self.ImportTextureFile(specRoughness, "SpecularRoughness")
            self.ImportTextureFile(displacement, "Displacement")
            self.ImportTextureFile(normal, "Normal")
            self.ImportTextureFile(presence, "Presence")
        elif(self.purpose == "previs"):
            self.ImportTextureFile(baseColor, "BaseColor")
            self.ImportTextureFile(metallic, "Metallic")
            self.ImportTextureFile(roughness, "Roughness")
            self.ImportTextureFile(normal, "Normal")
            self.ImportTextureFile(height, "Height")
        hou.ui.displayMessage("Finished building " + self.purpose + " shader for " +self.shaderName+".",buttons=("Okay",),title="Success!")