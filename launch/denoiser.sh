SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#Run the env.sh file
source $SOURCEDIR/env.sh
/usr/autodesk/maya2023/bin/mayapy /groups/unfamiliar/anim_pipeline/pipe/tools/standaloneTools/denoiser/ui.py