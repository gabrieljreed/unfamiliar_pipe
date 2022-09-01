import hou 
import os 

#This class asks the user for the location on disk of texture maps, then builds
#a basic shading network. It can create either previs (usdpreviewsurface) or prod
#(pxrsurface) shaders. 
#I want to build better error handling for this eventually, but in the meantime -
#if you're stuck, here are some common issues: 
    #texture maps do not have the exact same base name as the asset
    #textures were exported from substance painter with an incorrect export preset
    #filepath is incorrect 

class BuildShader():

    def defaultShaderBuild(filePath,fileFormat,UDIMs, purpose):
        folder = os.listdir(filePath)

        #define identifier according to purpose
        if(purpose == "prod"):
            identifier = "DiffuseColor"
            prefix = "pxr"
        #define variables for previs shader
        elif(purpose == "previs"):
            identifier = "BaseColor"
            prefix = "unreal"
            
        #determine shaderName
        named = 0
        for file in folder:     
            if((identifier in file) and (named == 0)):
                shaderName = file.split("_"+ identifier)[0]
                #remove spaces
                shaderName = shaderName.replace(" ","_")
                named = 1
                #hopefully this helps with debugging - if the shaderName 
                #the code thinks it has is not the one you think it should
                #have, take a closer look at exactly what file names you're
                #giving it 
                print("creating shader for "+shaderName)
            else: continue
            
            matLibLoc = "/stage/"+prefix+"_"+str(shaderName)+"/"
            if(matLibLoc == None):
                print("uh oh")
                print(matLibLoc) 
                print("yo there's a problem. Double check that you're pointing to the right "+
                "texture folder and that your texture files are named appropriately.")
            matLib = hou.node(matLibLoc)
            
            #Prep material library
            #cleanup network 
            toDelete = hou.vopNodeTypeCategory().nodeType("usdpreviewsurface").instances()
            #print(toDelete)
            if(len(toDelete)!= 0):
                toDelete[0].destroy()
            #define output collect
            if(hou.node(matLibLoc+"collect1") != None):
                outputCollect = hou.node(matLibLoc+"collect1")
            else: outputCollect = matLib.createNode("collect")
            
            #Create basic shading network 
            if(purpose == "prod"):
                #create pxrSurface and wire into output_collect
                pxrSurface = matLib.createNode("pxrsurface","pxr_"+shaderName)
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
                pxrSurface.setInput(103,normal,0)
                #displacement
                pxrDisplace = matLib.createNode("pxrdisplace")
                #note: this is just a starting place. you'll likely have to adjust it manually furthur)
                pxrDisplace.parm("dispAmount").set("0.015")
                outputCollect.setInput(1,pxrDisplace,0)
                pxrDispTransform = matLib.createNode("pxrdisptransform")
                #this is assuming your displacement map has a midpoint of 0.5 
                #(which if you're using substance painter usually it will)
                pxrDispTransform.parm("dispRemapMode").set("2")
                pxrDisplace.setInput(1,pxrDispTransform,1)
                displacement = matLib.createNode("pxrtexture","displacement_pxrtexture")
                pxrDispTransform.setInput(0,displacement,1)
                #layout nodes inside material library
                matLib.layoutChildren()
            elif(purpose == "previs"):
                #create primvar reader
                usdPrimvarReader = matLib.createNode("usdprimvarreader")
                usdPrimvarReader.parm("signature").set("float2")
                usdPrimvarReader.parm("varname").set("st")
                #create USD Preview Surface and wire into output_collect
                usdPrevSurface = matLib.createNode("usdpreviewsurface","unreal_"+shaderName)
                outputCollect.setInput(0,usdPrevSurface,0)
                #diffuse color
                diffuseColor = matLib.createNode("usduvtexture::2.0","diffuse_color_usduvtexture")
                diffuseColor.setInput(1,usdPrimvarReader,0)
                usdPrevSurface.setInput(0,diffuseColor,4)
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

            #Import texture image files
            def ImportTextureFile(mapTypeNode, mapTypeString):
                importedMap = 0
                for file in folder:
                    if(file.startswith(shaderName) and (mapTypeString in file) and file.endswith(fileFormat) and importedMap == 0):
                        #print ("importing the following file: " + str(file))
                        fullFilePath = filePath + "/" + str(file)
                        #print ("unmodified full file path is as follows: " + fullFilePath)
                        if(UDIMs == 1):
                            #SET FILE PATH USING UDIM SYNTAX
                            print("yes UDIMs")
                            #remove ".10**.png" and replace with ".<UDIM>.png"
                            splitIndex = fullFilePath.find(".10")
                            udimFilePath = fullFilePath[:splitIndex] + ".<UDIM>"+fileFormat
                            #set file path to correct UDIM syntax
                            if(purpose == "prod"):
                                mapTypeNode.parm("filename").set(udimFilePath)
                            elif(purpose == "previs"):
                                mapTypeNode.parm("file").set(udimFilePath)
                            #print ("UDIM file path is as follows: " + udimFilePath)
                        elif(UDIMs == 0):
                            print("no UDIMs")
                            #SET FILE PATH DEFAULT METHOD
                            if(purpose == "prod"):
                                mapTypeNode.parm("filename").set(fullFilePath)
                            elif(purpose == "previs"):
                                mapTypeNode.parm("file").set(fullFilePath)
                        importedMap = 1
            
            if(purpose == "prod"):
                ImportTextureFile(diffuseColor, "DiffuseColor")
                ImportTextureFile(specFaceColor, "SpecularFaceColor")
                ImportTextureFile(specRoughness, "SpecularRoughness")
                ImportTextureFile(displacement, "Displacement")
                ImportTextureFile(normal, "Normal")
            elif(purpose == "previs"):
                ImportTextureFile(diffuseColor, "BaseColor")
                ImportTextureFile(metallic, "Metallic")
                ImportTextureFile(roughness, "Roughness")
                ImportTextureFile(normal, "Normal")
                ImportTextureFile(height, "Height")
                
            #layout all shader nodes
            matLib.layoutChildren()
            #end function definitions
            #lol how do you even format this 
            #who knows
    ####################################################################################################

    #get texture folder and file format     
    #get filepath
    userInput = hou.ui.readInput("Copy and paste the path to the folder where you saved your " + 
    "texture files: ",buttons=("okay","close",),default_choice=0,title="import texture files")

    if (userInput[0] == 1):
        quit()
    filePath = userInput[1]

    #print ("unmodified filepath is: " + filePath)
    #change forward slashes to backslashes 
    filePath = filePath.replace("\\","/")
    #print("corrected relative filepath is: " + filePath)

    fileFormatNum = hou.ui.displayMessage("What file format did you use to save your texture " + 
    "files?",buttons=(".png",".jpg",".tif","close",),default_choice=0,title="import texture files")

    if(fileFormatNum == 0):
        fileFormat = ".png"
    elif(fileFormatNum == 1):
        fileFormat = ".jpg"
    elif(fileFormatNum == 2):
        fileFormat = ".tif"
    elif(fileFormatNum == 3):
        quit()

    UDIMs = hou.ui.displayMessage("Does this asset use UDIMs?",buttons=("No","Yes",),default_choice=0,
    title="import texture files")
    #print("UDIMs = " + str(UDIMs))

    purposeNum = hou.ui.displayMessage("Prod or previs?",buttons=("prod","previs","close"),default_choice=0,
    title="import texture files")
    if(purposeNum == 0):
        purpose = "prod"
    elif(purposeNum == 1):
        purpose = "previs"
    elif(purposeNum == 2):
        quit()

    defaultShaderBuild(filePath,fileFormat,UDIMs,purpose)