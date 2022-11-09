#First we run env.sh to get basic enviornment variables
#Get the directory this file is located in to reach env.sh
SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#Run the env.sh file
source $SOURCEDIR/env.sh

python3 $MEDIA_PROJECT_DIR/pipe/tools/checkoutList/houdini_checkout.py
