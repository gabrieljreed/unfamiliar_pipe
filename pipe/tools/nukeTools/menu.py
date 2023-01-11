"""This script runs when the Nuke UI is opened. It is NOT run when Nuke is started from the command line."""

import nuke

# Find the top level menu bar and add a custom menu to it
topLevelMenu = nuke.menu('Nuke')
unNukeMenu = topLevelMenu.addMenu('unNuke')

# unNukeMenu.addCommand("Test", "import sys; nuke.message(str(sys.path))")
unNukeMenu.addCommand("Shot Checkout", """import checkout.shot_checkout; ui = checkout.shot_checkout.ShotCheckout();
ui.show()""")
unNukeMenu.addCommand("Shot Publish", """import publish.shot_publish; ui = publish.shot_publish.ShotPublish();
ui.show()""")
unNukeMenu.addCommand("Shot Builder", """import AutoProjectSettings; AutoProjectSettings.SaveandClose()""",
                      "strl+shift+r")
unNukeMenu.addCommand("EXR Export", """import outputStuff; outputStuff.exrExport()""")
unNukeMenu.addCommand("MOV Export", """import outputStuff; outputStuff.movExport()""")

# Add custom formats here if you want I guess

nuke.Root()["colorManagement"].setValue("OCIO")
nuke.Root()["OCIO_config"].setValue("custom")
nuke.Root()["customOCIOConfigPath"].setValue("/opt/pixar/RenderManProServer-24.4/lib/ocio/ACES-1.2/config.ocio")
