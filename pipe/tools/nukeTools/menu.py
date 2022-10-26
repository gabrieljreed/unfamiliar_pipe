"""This script runs when the Nuke UI is opened. It is not run when Nuke is started from the command line."""

import nuke

# Not actually sure what this does, but it's in the Cenote pipe
from AutoProjectSettings import SaveandClose

# Find the top level menu bar and add a custom menu to it
topLevelMenu = nuke.menu('Nuke')
unNukeMenu = topLevelMenu.addMenu('unNuke')

unNukeMenu.addCommand("Test", "import sys; nuke.message(str(sys.path))")
# unNukeMenu.addCommand('Shot Checkout', 'checkout.shot_checkout.ShotCheckout().checkout()')
unNukeMenu.addCommand("Shot Checkout", "import checkout.shot_checkout; checkout.shot_checkout.ShotCheckout().checkout()")
# unNukeMenu.addCommand('Shot Checkout', lambda: import pipe; pipe.pipeTools.nukeTools.checkout.shot_checkout.ShotCheckout().checkout())

# Add custom formats here if you want I guess
