# BYU Unfamiliar Pipeline

## Description
This is a heavily modified version of the [previous pipeline](https://github.com/smartins1234/BYU_anm_pipeline) used on the Cenote film project, with many tools and improvements for the Unfamiliar film project. Improvements include: 
- Full adoption of USDs
- Use of Python 3

This pipeline has been developed on and for CentOS 7.

Asset management makes heavy use of the `groups` folder in the BYU CS server. Since every user has access to the groups folder, this pipeline does not have tools for sharing assets between users/computers.

## Table of Contents
- [Usage and features](https://github.com/gabrieljreed/unfamiliar_pipe#usage--features) (for artists)
  - [Maya](https://github.com/gabrieljreed/unfamiliar_pipe#maya)
  - [Houdini](https://github.com/gabrieljreed/unfamiliar_pipe#houdini)
  - [Nuke](https://github.com/gabrieljreed/unfamiliar_pipe#nuke)

- [Development](https://github.com/gabrieljreed/unfamiliar_pipe#development) (for programmers)
  - [Maya](https://github.com/gabrieljreed/unfamiliar_pipe#autodesk-maya-2023)
  - [Houdini](https://github.com/gabrieljreed/unfamiliar_pipe#sidefx-houdini-195)
  - [Nuke](https://github.com/gabrieljreed/unfamiliar_pipe#nuke-1)

## Usage & Features
### Maya
Unmaya can be started by running the script directly, (e.g. `/groups/unfamiliar/anim_pipeline/launch/maya.sh`) or clicking the unmaya icon in the `icons` folder.
#### Shelves
UnMaya provides several custom shelves with functionality specifically for Unfamiliar and other silly things.
- UnAnim
  - **Kelleth:** References the Kelleth rig into the current scene
  - **Maggie:** References the Maggie rig into the current scene
  - **Singe:** References the Singe rig into the current scene
  - **Dolls:** References the dolls rigs into the current scene
  - **Frog:** References the frog rig into the current scene
  - **Amogus:** References the Amogus rig into the current scene
  - **Previous Rig:** Launches a dialog to reference a previous version of a rig into current scene
  - **Layout:** Imports the USD layout into the current scene
  - **Cam:** ??
  - **Prod Ref:** Converts a selected prop in the USD layout into an FBX reference that can be animated on
  - **Ref:** Refreshes all prop references to their most recent USD version
  - **Export Alembic:** Launches a dialog to export the current shot as an alembic and publish it into the pipe
  - **StudioLibrary:** Loads the StudioLibrary plugin for animators
  - **Discord:** Launches the Maya to Discord tool
  - **AnimBot:** Loads the AnimBot plugin for animators
- UnPipe
- UnRig
  - **Publish:** Publishes a rig and versions it in its correct location within the `production` folder
- UnFiles
- UnDev
  - **Debug:** Launches a debug session using `debugpy` that can be attached to with VS Code. 
  - **Unload:** Unloads all python packages allowing for code refreshes without having to reopen Maya.
  - **Report:** Launches a dialog allowing the user to report an issue on the Github page. 
- UnPrevis

### Houdini


### Nuke



## Development
This pipeline consists of toolsets for several DCC packages. 

### Autodesk Maya 2023
The `maya.sh` file found in the `launch/` folder is a bash script that sets many environment variables and settings for Maya before launching it. 
The `userSetup.py` file located in the `pipe` folder sets up the custom shelves and keyboard shortcuts that turn Maya into the unmaya we all know and love.

It can be started by running the script directly, (e.g. `/groups/unfamiliar/anim_pipeline/launch/maya.sh`) or clicking the unmaya icon in the `icons` folder.

To add a new shelf, create a json file within `/pipe/tools/mayaTools/custom`. It will be automatically detected when unmaya launches. 

To add a button to the shelf, add a new JSON entry (see other buttons for examples). It will be automatically detected when unmaya launches. Button icons are located in the `icons` folder and should be pathed relative to that folder (e.g. an icon located at `/icons/discordIcons/desktop.png` should have its path provided as `"discordIcons/desktop.png"`)

To create a new keyboard shortcut, add a new entry to `/pipe/tools/mayaTools/UnDev/setupHotkeys.py` at the bottom of the file such that it is added to the unfamiliarHotkeySet. Make sure to not overwrite any existing keyboard shortcuts, since this change will propogate to everybody and could destroy expected functionality.

### SideFX Houdini 19.5

### Nuke