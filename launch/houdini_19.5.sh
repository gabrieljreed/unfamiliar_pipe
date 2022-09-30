#This file creates all the environment variables needed for our film's houdini pipeline

#First we run env.sh to get basic enviornment variables
#Get the directory this file is located in to reach env.sh
SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#Run the env.sh file
source $SOURCEDIR/env.sh

#Set the JOB directory
export JOB=${MEDIA_PROJECT_DIR}/production

#houdiniTools directory path that will be used in following export commands
HOUDINI_TOOLS=${MEDIA_PIPE_DIR}/tools/houdiniTools

#Add the houdini tools folder to the pythonpath for easy access
export PYTHONPATH=${PYTHONPATH}:${HOUDINI_TOOLS}

#Update HOUDINI_PATH to include custom tools and menus
export HOUDINI_PATH=${HOUDINI_PATH}:${HOUDINI_TOOLS}:${HOUDINI_TOOLS}"/custom;&":${HOUDINI_TOOLS}"/custom/hda;&"

#Add custom menu, desktop, toolbar, and icon paths
export HOUDINI_MENU_PATH=${HOUDINI_TOOLS}"/custom/menu;&"
export HOUDINI_DESK_PATH=${HOUDINI_MENU_PATH}
export HOUDINI_TOOLBAR_PATH=${HOUDINI_TOOLS}"/custom/toolbar;&"
export HOUDINI_UI_ICON_PATH=${MEDIA_PROJECT_DIR}"/icons;&"

#Update HSITE for startup script
export HSITE=${HOUDINI_TOOLS}"/custom/HSITE/houdini19.0;&"

#Add path to hda assets
export HOUDINI_OTLSCAN_PATH=${HOUDINI_TOOLS}"/custom/hda;&"

#Start Houdini
echo "Starting Houdini..."
/opt/hfs19.5.303/bin/houdinifx -foreground -desktop UnSolaris $@ &

