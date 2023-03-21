import os


sourcePath = "/groups/unfamiliar/anim_pipeline/icons/MayaEDUStartupImage.png"


if __name__ == "__main__":
    # Get the user's home directory
    homeDir = os.path.expanduser("~")
    homeDir = os.path.join(homeDir, "maya", "2023", "prefs", "icons")
    print(homeDir)
    print(os.path.isdir(homeDir))

    # Copy the image to the user's home directory
    if os.path.isdir(homeDir):
        os.system("cp %s %s" % (sourcePath, homeDir))

    print("Done!")
