import hou
import os

class PropClusterSetup():

    def __init__(self):
        #CHANGE THESE TWO VARIABLES TO POINT AT YOUR IMPORT AND EXPORT LOCATIONS
        self.importFilePath = "/groups/unfamiliar/shading/Anna/ceiling/CeilingUSD"
        self.exportFilePath = "/groups/unfamiliar/shading/Anna/ceiling/CeilingFBX"

    def BuildCluster(self):
        stage = hou.node("/stage")
        #create container geo node 
        containerNode = stage.createNode("sopnet",node_name="prop_layout")
        #print(containerNode)
        #containerNode.allowEditingOfContents()
        null = containerNode.createNode("null")
        null.destroy()
        #create merge node
        mergeNode = containerNode.createNode("merge")

        #pull the files from the folder into a list of files 
        filesToImport = os.listdir(self.importFilePath)
        counter = 0

        for file in filesToImport:
            #create file node
            curFileNode = containerNode.createNode("file",str(file)+"GEO")
            curFileNode.parm("file").set(self.importFilePath+"/"+str(file))

            curGeoName = file.replace("prod_","")
            curGeoName = curGeoName.replace(".usd","")
            #print(curGeoName)

            curUnpackNode = containerNode.createNode("unpackusd::2.0")
            curUnpackNode.parm("output").set(1)
            curUnpackNode.setInput(0,curFileNode,0)

            curUnwrapNode = containerNode.createNode("uvunwrap")
            curUnwrapNode.setInput(0,curUnpackNode,0)

            curUvLayoutNode = containerNode.createNode("uvlayout")
            curUvLayoutNode.setInput(0,curUnwrapNode,0)

            curAttCr = containerNode.createNode("attribcreate")
            curAttCr.parm("type1").set("index")
            curAttCr.parm("name1").set("shop_materialpath")
            curAttCr.parm("class1").set("primitive")
            curAttCr.parm("string1").set(curGeoName)
            curAttCr.setInput(0,curUvLayoutNode)

            curRop = containerNode.createNode("rop_fbx")
            curRop.parm("sopoutput").set(self.exportFilePath+"/"+curGeoName+".fbx")
            curRop.setInput(0,curAttCr,0)
            curRop.parm("execute").pressButton()

            mergeNode.setInput(counter,curAttCr,0)
            counter+=1

        alignDist = containerNode.createNode("align_and_distribute")
        alignDist.parm("split_by").set(1)
        alignDist.parm("attribname").set("shop_materialpath")
        alignDist.setInput(0,mergeNode,0)
        alignDist.setDisplayFlag(True)

        output = containerNode.createNode("output","OUT_PROP_LAYOUT")
        output.setInput(0,alignDist,0)
        output.setDisplayFlag(True)

        finalRop = containerNode.createNode("rop_fbx")
        finalRop.parm("sopoutput").set(self.exportFilePath+"/prop_layout.fbx")
        finalRop.setInput(0,alignDist,0)
        finalRop.parm("execute").pressButton()

        #visualize lol. pretty sure there is a viewport bug happening here
        #so ... this is the workaround
        #rip
        viewer = stage.createNode("sopimport","VIEWER")
        viewer.parm("soppath").set("/stage/"+containerNode.name()+"/OUT_PROP_LAYOUT/")

        #layout nodes
        containerNode.layoutChildren()
        stage.layoutChildren()