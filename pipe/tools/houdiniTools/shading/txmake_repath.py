from fileinput import filename
from xml.dom.expatbuilder import TEXT_NODE
import hou 
import os 

#Run this after running txmake (yes, we have to do it manually in Houdini 19 and 
# Renderman 24.4) (: to repath the textures. You only have to do this on the 
#pxrsurface shaders - the usdpreviewsurface ones don't need it.

class TxmakeRepath():
    FILETYPE = ".png"
    stage = hou.node("/stage/")
    stageNodes = stage.children()

    def GetNodesToUpdate(self):
        matLibNodes = []
        #get all material library nodes in stage
        for node in self.stageNodes:
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
        return pxrTexNodes
    
    def UpdateFilename(self,texNode, ogFilename, newSuffix):
        if("UDIM" not in ogFilename):
            newFilename = ogFilename.replace(".png",newSuffix)
        elif("UDIM" in ogFilename):
            splitIndex = ogFilename.find(".<UDIM>")
            suffixSplitIndex = newSuffix.find(".png")
            finalSuffix = newSuffix[:suffixSplitIndex]+".<UDIM>"+newSuffix[suffixSplitIndex:]
            newFilename = ogFilename[:splitIndex]+finalSuffix
        texNode.parm("filename").set(newFilename)

    def RepathTextures(self,nodesToUpdate):
        #update each filename to point to the tex file (accounting for UDIMs) 
        for texNode in nodesToUpdate:
            #check that filename hasn't already been updated
            filenameParm = texNode.parm("filename").eval()
            if("acescg" not in filenameParm):
                if("Normal" not in filenameParm and "SpecularRoughness" not in filenameParm):  
                    self.UpdateFilename(texNode,filenameParm,"_srgbtex_acescg.png.tex")
                elif("Normal" in filenameParm or "SpecularRoughness" in filenameParm):
                    self.UpdateFilename(texNode,filenameParm,"_data_acescg.png.tex")