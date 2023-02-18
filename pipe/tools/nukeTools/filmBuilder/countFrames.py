import subprocess


def countFrames(path):
    s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=nb_read_frames", "-print_format", "csv", path], stdout=subprocess.PIPE)
    result = int(s.stdout.decode().split(",")[1])
    return result


if __name__ == "__main__":
    videoFilePath = "/groups/unfamiliar/anim_pipeline/production/edit/shots/02_anim_playblast/A_010/A_010.mov"
    totalFrames = countFrames(videoFilePath)
    print(f"Total frames: {totalFrames}")
