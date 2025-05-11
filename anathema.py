#!/usr/bin/python3

import os
import random
import sys
import time

IS_WINDOWS = (os.name == "nt")
IS_MAC = sys.platform == "darwin"

if IS_WINDOWS:
    import winsound

#################
##  FUNCTIONS  ##
#################

def printrules(rules):
    with open(rules, "r") as f:
        print(f.read())

def parseline(line):
    """ All-purpose parsing routine.
        Returns empty string if line has no word. """
    parsedline = line.strip().split()
    if parsedline:
        return line.strip()
    return ""

def playsound(soundfile):
    if IS_WINDOWS:
        winsound.PlaySound(soundfile, winsound.SND_FILENAME)
    elif IS_MAC:
        os.system(f'afplay "{soundfile}" &')

def pauseround():
    playsound(sound_endround)
    print("\n\n\n\n")
    input("[ROUND OVER] Press enter to continue.")

def playround(filename, roundtime):
    global wordarray
    global endround

    if filename:
        print(f"[Opening file: {filename}]")
        wordarray = []
        with open(filename, "r", encoding="utf-8") as wordfile:
            for line in wordfile:
                addword = parseline(line)
                if addword:
                    wordarray.append(addword)
    endround = time.time() + roundtime

    while wordarray and time.time() < endround:
        print("\n\n\n\n")
        nextindex = random.randint(0, len(wordarray) - 1)
        nextword = wordarray.pop(nextindex)
        print(nextword)
        print("=" * len(nextword))

        input("Press enter for next word: ")

        remaining = int(endround - time.time())
        print(f"Time left: {remaining // 60}:{remaining % 60:02d}")

    pauseround()
    print("[GAME OVER] End of one round.")

def read_wordfile(filepath):
    wordarray = []
    try:
        with open(filepath, "r", encoding="utf-8") as wordfile:
            for line in wordfile:
                addword = parseline(line)
                if addword:
                    wordarray.append(addword)
    except UnicodeDecodeError:
        print(f"[Warning] UnicodeDecodeError when reading {filepath}. Trying with ISO-8859-1 encoding.")
        with open(filepath, "r", encoding="ISO-8859-1") as wordfile:
            for line in wordfile:
                addword = parseline(line)
                if addword:
                    wordarray.append(addword)
    return wordarray


############
##  GAME  ##
############

roundtime = 60.0 * 3  # default 3 minutes
wordlist_directories = ["wordlists"]

sound_endround = os.path.join("sounds", "redalert.wav")
rulesfile = "rules.txt"

printrules(rulesfile)

# Prompt for chaos mode
chaos_mode = input("Enable chaos mode? (y/n, default: n): ").strip().lower()
if chaos_mode == 'y':
    chaos_mode = True
else:
    chaos_mode = False

try:
    roundtime = float(input("Set round length (default 180s): "))
except ValueError:
    print("Defaulting to " + str(roundtime) + " seconds")

try:
    num_rounds = int(input("Number of rounds (default 3): "))
    if num_rounds < 1:
        raise ValueError
except ValueError:
    print("Defaulting to 3 rounds")
    num_rounds = 3

filelist = []
if not chaos_mode:
    for worddir in wordlist_directories:
        if os.path.isdir(worddir):
            filelist += [os.path.join(worddir, x) for x in os.listdir(worddir) if os.path.isfile(os.path.join(worddir, x))]

    if not filelist:
        print("[Error] No word files found. Exiting.")
        sys.exit(1)

# Chaos mode: Combine all words into one large list
if chaos_mode:
    print("[Chaos Mode] Building one huge word list from all available word files.")
    wordarray = []
    for worddir in wordlist_directories:
        if os.path.isdir(worddir):
            for file in os.listdir(worddir):
                filepath = os.path.join(worddir, file)
                if os.path.isfile(filepath):
                    wordarray.extend(read_wordfile(filepath))  # Use the new function
    if not wordarray:
        print("[Error] No words found in any word files. Exiting.")
        sys.exit(1)

else:
    # Show available word files for non-chaos mode
    for i, file in enumerate(filelist):
        print(f"[{i:2d}]  {file}")

    filename = ""
    while True:
        try:
            filenumber = int(input("Enter index of file to open: "))
            if 0 <= filenumber < len(filelist):
                filename = filelist[filenumber]
                break
            else:
                print("[index out of range]")
        except ValueError:
            print("[input was not a number]")

for round_num in range(1, num_rounds + 1):
    print(f"\n=== ROUND {round_num} of {num_rounds} ===")
    if chaos_mode:
        print("[Chaos Mode] Random word from combined list.")
        playround(None, roundtime)  # Pass None instead of filename
    else:
        playround(filename, roundtime)


print("\nAll rounds completed.")
input("Press enter to quit: ")
