#This file creates all the environment variables needed for our film's nuke pipeline

#First we run env.sh to get basic enviornment variables
#Get the directory this file is located in to reach env.sh
SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#Run the env.sh file
source $SOURCEDIR/env.sh

export NUKE_PATH=${MEDIA_PROJECT_DIR}/pipe:${MEDIA_PROJECT_DIR}/pipe/tools/nukeTools:${MEDIA_PROJECT_DIR}/lib/NukeSurvivalToolkit

/opt/Nuke13.2v2/Nuke13.2 --nukex

