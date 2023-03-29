"""Command-line tool to export a temp mp4 from a nuke script."""
import argparse
import os


productionShotsDir = r"/groups/unfamiliar/anim_pipeline/production/shots"


def listShots(filter=None) -> list:
    """List all shots in the production directory.

    Arguments:
        filter {str} -- Filter the shots by this string. (default: {None})

    Returns:
        list -- List of shots.
    """
    shots = os.listdir(productionShotsDir)
    badShotNames = ["turnaround", "render_card", "OLD_SHOTS"]
    shots = [shot for shot in shots if all(badShot not in shot for badShot in badShotNames)]
    shots.sort()

    if filter:
        shots = [shot for shot in shots if filter in shot]

    return shots


def main(shot):
    """Run the main function.

    Arguments:
        shot {str} -- Shot to export.
    """
    command = """
export MEDIA_PROJECT_DIR=/groups/unfamiliar/anim_pipeline
export MEDIA_PIPE_DIR=$MEDIA_PROJECT_DIR/pipe
#Environment variable for location of python scripts
export PYTHONPATH=${MEDIA_PROJECT_DIR}:${MEDIA_PIPE_DIR}:${MEDIA_PROJECT_DIR}/lib/
unset OCIO

export NUKE_PATH=${MEDIA_PROJECT_DIR}/pipe:${MEDIA_PROJECT_DIR}/pipe/tools/nukeTools:${MEDIA_PROJECT_DIR}/lib/NukeSurvivalToolkit

        """

    pythonFile = os.path.normpath(os.path.join(os.path.dirname(__file__), "export.py"))

    lastLine = f"/opt/Nuke13.2v2/Nuke13.2 -t {pythonFile} {shot}"
    command += "\n" + lastLine

    print(command)
    os.system(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--shot", help="shot to export", type=str)
    parser.add_argument("-l", "--list", help="list shots", action="store_true")

    args = parser.parse_args()

    if args.list:
        shots = listShots(filter=args.shot)
        print(f"Shots:")
        for shot in shots:
            print(f"\t{shot}")
        exit(0)

    if not args.shot:
        print("Please specify a shot to export.")
        exit(1)

    main(args.shot)
