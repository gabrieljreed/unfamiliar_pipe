import hou 
import os 

#Run this after running txmake (yes, we have to do it manually in Houdini 19 and 
# Renderman 24.4) (: to repath the textures. You only have to do this on the 
#pxrsurface shaders - the usdpreviewsurface ones don't need it.

class TxmakeRepath():
    stage = hou.node("/stage/")
    stageNodes = stage.children()

    matLibNodes = []
    #get all material library nodes in stage
    for node in stageNodes:
        if(node.name().startswith("pxr")):
            matLibNodes.append(node)
            #print(matLibNodes)
            
    #for each material library node... 
    for matLibNode in matLibNodes:
        #get all children
        matLibChildren = matLibNode.children()
        
        #determine which are pxrtextures and add to a list
        pxrTexNodes = []
        for node in matLibChildren:
            if("pxrtexture::3.0" in str(node.type())):
                pxrTexNodes.append(node)
            #and the normal map! 
            elif("pxrnormalmap::3.0" in str(node.type())):
                pxrTexNodes.append(node)
                
        #update each filename to point to the tex file (accounting for UDIMs) 
        for texNode in pxrTexNodes:
            #check that filename hasn't already been updated
            if("_srgbtex_acescg" not in texNode.parm("filename").eval()):
                print("its fixin time")
                ogFilename = texNode.parm("filename").eval()
                #default update
                if("UDIM" not in ogFilename):
                    print("default update")
                    newFilename = ogFilename.replace(".png","_srgbtex_acescg.png.tex")
                    texNode.parm("filename").set(newFilename)
                #UDIM update
                elif("UDIM" in ogFilename):
                    print("update UDIMs")
                    splitIndex = ogFilename.find(".<UDIM>")
                    newFilename = ogFilename[:splitIndex] + "_srgbtex_acescg.<UDIM>.png.tex"
                    texNode.parm("filename").set(newFilename)