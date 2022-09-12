#This file exports base project directories used by both the maya and houdini sh scripts.
#It is called by both the houdini.sh and maya.sh files.
#Future pipe artists should change these base directories to there own project paths.
#Depending on how future projects are set up, other directories might have to be re-routed.

#Enviornment variables for the main folder and pipe script locations
export MEDIA_PROJECT_DIR=/groups/unfamiliar/anim_pipeline
export MEDIA_PIPE_DIR=$MEDIA_PROJECT_DIR/pipe
#Environment variable for location of python scripts
export PYTHONPATH=${MEDIA_PROJECT_DIR}:${MEDIA_PIPE_DIR}:${MEDIA_PROJECT_DIR}/lib/

