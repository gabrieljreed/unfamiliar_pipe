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
    self.PREVIS_INPUT = '1'
    self.PROD_INPUT = '2'
    self.BOTH_INPUT = '3'
    self.PREVIS_INPUT_STRING = 'previs'
    self.PROD_INPUT_STRING = 'prod'
    self.BOTH_INPUT_STRING = 'both'

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
    self.item_gui = gui.SelectFromList(inputList=self.asset_list, parent=hou.ui.mainQtWindow(), title="Select a model to overwrite")
    #Send results from gui to the results method
    self.item_gui.submitted.connect(self.results)


  #Is called after the user interacts with the gui
  def results(self, value):
    self.ASSET_NAME = value[0]
    #Get asset type
    asset_type = self.assetType()
    if asset_type is not None:
      #Create the node network
      if asset_type == self.BOTH_INPUT:
        self.createNodeNetwork('previs')
        self.createNodeNetwork('prod')
      elif asset_type == self.PREVIS_INPUT:
        self.createNodeNetwork('previs')
      elif asset_type == self.PROD_INPUT:
        self.createNodeNetwork('prod')

  #Gets asset type from user input
  def assetType(self):
    asset_type = hou.ui.readInput("Valid inputs: \n \'%s\' or \'previs\',\n \'%s\' or \'prod\', \n \'%s\' or \'both\'" % (self.PREVIS_INPUT, self.PROD_INPUT, self.BOTH_INPUT))[1]

    #set so string input still workd
    if asset_type == self.PREVIS_INPUT_STRING:
      asset_type = self.PREVIS_INPUT
    elif asset_type == self.PROD_INPUT_STRING:
      asset_type = self.PROD_INPUT
    elif asset_type == self.BOTH_INPUT_STRING:
      asset_type = self.BOTH_INPUT

    if (asset_type != self.PREVIS_INPUT and asset_type != self.PROD_INPUT and asset_type != self.BOTH_INPUT):
      hou.ui.displayMessage("Invaild asset type. Please try again")
      print(asset_type)
      return None
    return asset_type
        
        
  def createNodeNetwork(self,asset_type):
    #If you are reading these notes im sorry I dont have the time to make this super good
    #but if you understand basic houdini python API it should be pretty strait forward

    #required 'global' variables
    ASSET_TYPE = asset_type
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
