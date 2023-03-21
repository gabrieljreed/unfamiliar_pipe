"""Check if Kelleth is in shots."""

import os


shotDir = r"/groups/unfamiliar/anim_pipeline/production/shots"

if __name__ == "__main__":
    sequencesToCheck = ["F", "I"]

    shots = os.listdir(shotDir)
    shots.sort()
    for shot in shots:
        renderDir = os.path.join(shotDir, shot, "render")

        if shot[0] not in sequencesToCheck:
            continue

        if not os.path.exists(renderDir):
            continue

        listdir = os.listdir(renderDir)
        listdir = [item.lower() for item in listdir]
        if "kelleth" in listdir:
            print(f"Kelleth in {shot}")
