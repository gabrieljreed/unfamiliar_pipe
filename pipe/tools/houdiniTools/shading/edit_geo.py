import hou
import pipe.pipeHandlers.gui as gui
from pipe.pipeHandlers.environment import Environment as env


#This class makes a gui for decided which shader to edit as well as making the 
#correct editing LOP node network
class EditGeo():

    def __init__(self):
        #Get asset list
        self.ASSET_PATH = env().get_asset_dir()
        self.asset_list = env().get_asset_list()
             
   
    def manual_call(self, assetname, assettype):
        self.ASSET_TYPE = assettype
        self.ASSET_NAME = assetname
        self.createNodeNetwork()


    #Function called by the "Edit Model" button in houdini
    def assetSelect(self):
        #Get asset name and type
        self.itemSelectGui()
        

    #Starts the gui for choosing asset
    def itemSelectGui(self):
        #Intilize gui with the asset list
        self.item_gui = gui.SelectFromList(l=self.asset_list, parent=hou.ui.mainQtWindow(), title="Select a model to overwrite")
        #Send results from gui to the results method
        self.item_gui.submitted.connect(self.results)


    #Is called after the user interacts with the gui
    def results(self, value):
        self.ASSET_NAME = value[0]
        #Get asset type
        if self.assetType():
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
        #If you are reading these notes im sorry I dont have the time to make this super good
        #but if you understand basic houdini python API it should be pretty strait forward

        #required 'global' variables
        ASSET_TYPE = self.ASSET_TYPE
        ASSET_NAME = self.ASSET_NAME
        ASSET_DIR = self.ASSET_PATH
        ASSET_PATH = ASSET_DIR + "/" + ASSET_NAME + "/geo/" + ASSET_TYPE + "_" + ASSET_NAME + ".usd"

        #Create the node setup
        stage = hou.node("/stage")

        #USD path
        usdPath = "/" + ASSET_NAME + "/geo/" + ASSET_TYPE + "_" + ASSET_NAME

        #Create sop create node and set needed parameters
        sopCreate01 = stage.createNode("sopcreate", node_name = ASSET_TYPE + '_' + ASSET_NAME)
        sopCreate01.parm("asreference").set(True)
        sopCreate01.parm("primpath").set(usdPath)
        sopCreate01.parm("parentprimkind").set("component")
        sopCreate01.parm("enable_pathprefix").set(False)
        sopCreate01.parm("enable_savepath").set(True)
        sopCreate01.parm("savepath").set(ASSET_DIR + usdPath + ".usd")
        sopCreate01.parm("authortimesamples").set("never")
        #yo anna here. adding this bit to turn on render-time subdivisions by default 
        #shouldn't cause issues unless models are crazy high poly but should save us 
        #a lot of annoyance from having to do it manually per-asset. 
        sopCreate01.parm("enable_polygonsassubd").set(1)
        sopCreate01.parm("polygonsassubd").set(1)

        #Get sop create subnet
        createNet01 = hou.node("/stage/" + sopCreate01.name() + "/sopnet/create")

        #Make necissary node network and set needed parameters
        usdImport01 = createNet01.createNode("usdimport")
        usdImport01.parm("filepath1").set(ASSET_PATH)
        usdImport01.parm("pivot").set("origin")
        usdImport01.parm("input_unpack").set(True)
        usdImport01.parm("unpack_geomtype").set("polygons")

        insertNull = createNet01.createNode("null", node_name = "INSERT_GEO_HERE")

        stopNull = createNet01.createNode("null", node_name = "DO_NOT_EDIT_BEYOND_THIS_NODE")

        attribDelete01 = createNet01.createNode("attribdelete")
        attribDelete01.parm("ptdel").set("*")
        attribDelete01.parm("primdel").set("*")
        attribDelete01.parm("dtldel").set("*")
        attribDelete01.setInput(0, usdImport01, 0)

        outNull = createNet01.createNode("null", node_name = "OUT")
        outNull.setDisplayFlag(True)

        outNull.setInput(0, attribDelete01, 0)
        attribDelete01.setInput(0, stopNull, 0)
        stopNull.setInput(0, insertNull, 0)
        insertNull.setInput(0, usdImport01, 0)

        createNet01.layoutChildren()

        #Connect to a usd rop
        usdRop = stage.createNode("usd_rop", node_name = "EXPORT_MODEL")
        usdRop.parm("lopoutput").set("/groups/unfamiliar/modeling/throwaway_usd/" + ASSET_NAME + "_delete.usda")
        usdRop.setInput(0, sopCreate01, 0)

        stage.layoutChildren()
