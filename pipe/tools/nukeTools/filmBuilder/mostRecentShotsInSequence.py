"""Print the most recent versions of all shots in a given sequence."""

import filmBuilder as fb


if __name__ == "__main__":
    # Get input from the user
    sequence = input("Enter the name of a sequence: (Enter 'film' to check all sequences)\n")
    sequence = sequence.upper()

    if "FILM" in sequence:
        print("Building entire film")
        for sq in fb.sequences:
            fb.mostRecentShotsInSequence(sq, includeTempMp4=True)
        exit()

    fb.mostRecentShotsInSequence(sequence, includeTempMp4=True)
