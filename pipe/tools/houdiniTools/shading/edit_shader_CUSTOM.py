import hou 
#FIX A BUNCH OF GARBBAGE
'''
okay I don't know why but when you reopen the shader for editing, it
messes up all the filepaths and also deactivates every single 
parameter. So this section activates all the parameters and 
corrects the filepaths. 
'''
matLibChildren = hou.node("/stage/pxr_frog").children()
basePath = "$JOB/assets/frog/materials/textures/"
#basePath = "$JOB/assets/"+assetName+"/materials/textures/"

#activate all parameters 
for node in matLibChildren:
    allParms = node.parms()

    activationParms = []
    for parm in allParms:                    
        if("__activate__" in str(parm)):
            parmName = str(parm).split(" ")[1]
            activationParms.append(parmName)
        #print("activationParms:")
        #print(activationParms)
        
        for activationParm in activationParms:
            node.parm(activationParm).set(1)

#fix filepaths
#get pxrtextures
pxrTexNodes = []
for node in matLibChildren:
    if("pxrtexture::3.0" in str(node.type())):
        pxrTexNodes.append(node)
    #and the normal map! 
    elif("pxrnormalmap::3.0" in str(node.type())):
        pxrTexNodes.append(node)
#fix each filepath
for texNode in pxrTexNodes:
    #print("fixing a filepath in a pxrtexture")
    #check that filename hasn't already been fixed
    if(texNode.parm("filename").eval().startswith("./textures")):
        ogFilename = texNode.parm("filename").eval()
        newFilename = ogFilename.replace("./textures/",basePath)
        texNode.parm("filename").set(newFilename)

#get usduvtextures 
usdUvNodes = []
for node in matLibChildren:
    #print(node.type())
    if("usduvtexture::2.0" in str(node.type())):
        usdUvNodes.append(node)
#print(usdUvNodes)
        
#fix each filepath
for uvNode in usdUvNodes:
    #print("fixing a usd uv texture node")
    #activate filename parameter
    uvNode.parm("__activate__file").set(1)
    #activate scale and bias(for displacement)
    uvNode.parm("__activate__scale").set(1)
    uvNode.parm("__activate__bias").set(1)
    ogFilePath = uvNode.parm("file").eval()
    FileName = ogFilePath.split('/')[-1]
    newFilePath = "$JOB/assets/"+ASSET_NAME+"/materials/textures/PBRMR/"+FileName
    uvNode.parm("file").set(newFilePath)