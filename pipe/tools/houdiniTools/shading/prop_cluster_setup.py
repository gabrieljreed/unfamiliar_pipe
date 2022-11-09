import hou
import os

class PropClusterSetup():

    def __init__(self):
        #CHANGE THESE TWO VARIABLES TO POINT AT YOUR IMPORT AND EXPORT LOCATIONS
        self.importFilePath = "/groups/unfamiliar/shading/Anna/AssetsUnclaimed/KitchenTable/KitchenTableUSD"
        self.exportFilePath = "/groups/unfamiliar/shading/Anna/AssetsUnclaimed/KitchenTable/KitchenTableFBX"
        self.clusterName = "KitchenTable"

    def BuildCluster(self):
        stage = hou.node("/stage")
        obj = hou.node("/obj")
        #create container geo node 
        containerNode = obj.createNode("geo",node_name="prop_layout")
        #create merge node
        mergeNode = containerNode.createNode("merge")

        #pull the files from the folder into a list of files 
        filesToImport = os.listdir(self.importFilePath)
        counter = 0

        for file in filesToImport:
            #create file node
            print("file = " + str(file))
            FileNode = containerNode.createNode("file",str(file)+"GEO")
            FileNode.parm("file").set(self.importFilePath+"/"+str(file))

            GeoName = file.replace("prod_","")
            GeoName = GeoName.replace(".usd","")
            #print(GeoName)

            unpack = containerNode.createNode("unpackusd::2.0")
            unpack.parm("output").set(1)
            unpack.setInput(0,FileNode,0)

            unwrap = containerNode.createNode("uvunwrap")
            unwrap.setInput(0,unpack,0)

            uvLayout = containerNode.createNode("uvlayout")
            uvLayout.setInput(0,unwrap,0)

            attCr = containerNode.createNode("attribcreate")
            attCr.parm("type1").set("index")
            attCr.parm("name1").set("shop_materialpath")
            attCr.parm("class1").set("primitive")
            attCr.parm("string1").set(GeoName)
            attCr.setInput(0,uvLayout,0)

            softenNormals = containerNode.createNode("labs::soften_normals")
            softenNormals.setInput(0,attCr,0)

            rop = containerNode.createNode("rop_fbx")
            rop.parm("sopoutput").set(self.exportFilePath+"/"+GeoName+".fbx")
            rop.setInput(0,softenNormals,0)
            rop.parm("execute").pressButton()

            mergeNode.setInput(counter,softenNormals,0)
            counter+=1

        alignDist = containerNode.createNode("align_and_distribute")
        alignDist.parm("split_by").set(1)
        alignDist.parm("attribname").set("shop_materialpath")
        alignDist.setInput(0,mergeNode,0)
        alignDist.setDisplayFlag(True)

        subdivide = containerNode.createNode("subdivide")
        subdivide.setInput(0,alignDist,0)

        output = containerNode.createNode("output", self.clusterName + "_prop_layout")
        output.setInput(0,subdivide,0)
        output.setDisplayFlag(True)

        finalRop = containerNode.createNode("rop_fbx")
        finalRop.parm("sopoutput").set(self.exportFilePath+"/" + self.clusterName + "_prop_layout.fbx")
        finalRop.setInput(0,output,0)
        finalRop.parm("execute").pressButton()
        
        #layout nodes
        containerNode.layoutChildren()
        stage.layoutChildren()