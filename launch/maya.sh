#This file creates all the environment variables needed for our film's maya pipeline

#First we run env.sh to get basic enviornment variables
#Get the directory this file is located in to reach env.sh
SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#Run the env.sh file
source $SOURCEDIR/env.sh

#Export the maya shelf and icon directories
export MAYA_SHELF_DIR=${MEDIA_PROJECT_DIR}'/pipe/tools/mayaTools/custom/'

#Export the script paths
export MAYA_SCRIPT_PATH=${MAYA_SCRIPT_PATH}:${MEDIA_PROJECT_DIR}'/pipe/tools/mayaTools/scripts/':${MEDIA_PROJECT_DIR}'/pipe/tools/mayaTools/vendor/'

#Export the maya USD environment variables
export MAYAUSD_EXPORT_MAP1_AS_PRIMARY_UV_SET=1
export MAYAUSD_IMPORT_PRIMARY_UV_SET_AS_MAP1=1

#Export the maya ICON directory to be used when creating shelves
export MAYA_ICONS_DIR=${MEDIA_PROJECT_DIR}'/icons/'

#WE HATE ACES
unset OCIO

#Start Maya
echo "Starting Maya..."
maya #-script ${MEDIA_PROJECT_DIR}/pipe/tools/mayaTools/custom/shelf.mel &



#Environment variables I didn't find needed but too afraid to delete them just in case
#this does eventually break the icons:

#export XBMLANGPATH=${XBMLANGPATH}:${MEDIA_PROJECT_DIR}'/icons/%B'
