#!/bin/sh

Help()
{
    #Display Usage
    echo "Usage: $0 -in path/to/input/dir -out path/to/output/dir"
    echo
    echo "options:"
    echo "-i    Directory containing the images to be denoised. Defaults to the current working directory."
    echo "-o    Destination for the denoised images. Defaults to a new directory based on the input directory."
    echo "-s    Denoising strength. Defaults to 0.5"
    echo "-v    Indicates that these are volume only frames."
    echo
}

indir=""
outdir=""
strength="0.5"
volume=0

while getopts "i:o:s:vh" opt; do
    case $opt in
        i)
            indir=$OPTARG
            ;;
        o)
            outdir=$OPTARG
            ;;
        s)
            strength=$OPTARG
            ;;
        v)
            volume=1
            ;;
        h)
            Help
            exit 0
            ;; 
        *)
            echo "Error: incorrect sytax"
            Help >&2
            exit 1
            ;;
    esac
done

if [ -z "$indir" ]
then
    indir="$(pwd)"
fi

if [ -z "$outdir" ]
then
    outdir=${indir}
    outdir=${outdir}_denoised
fi

echo "$indir"
echo "$outdir"

SOURCEDIR=/groups/cenote/BYU_anm_pipeline/launch
echo "$SOURCEDIR"
source $SOURCEDIR/env.sh

export RMANTREE="/opt/pixar/RenderManProServer-24.1"
export PATH=PATH:"/opt/pixar/RenderManProServer-24.1/bin"

echo "strength: $strength"

if [ $volume -eq 1 ]
then
    denoise --crossframe --override filterbanks.*.strength $strength -f /opt/pixar/RenderManProServer-24.1/lib/denoise/volume.filter.json -o denoised --outdir $outdir -v variance ${indir}/*.exr
else
    denoise --crossframe --override filterbanks.*.strength $strength -o denoised --outdir $outdir -v variance ${indir}/*.exr
fi