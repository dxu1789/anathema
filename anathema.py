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

def savegame(savename):
    global wordarray
    if not savename.strip():
        print("[Error] Save name given is empty.")
        return
    try:
        os.makedirs(saves_directory, exist_ok=True)
        safe_name = "".join(c for c in savename if c.isalnum() or c in (' ', '_', '-')).strip()
        savetarget = os.path.join(saves_directory, safe_name + ".txt")
        print(f"[Saving] {savetarget}")
        with open(savetarget, "w") as f:
            for s in wordarray:
                f.write(s + "\n")
        print("[Game saved]")
    except IOError as e:
        print(f"[Error] Failed to save: {e}")

def playround(filename, roundtime):
    global wordarray
    global endround

    print(f"[Opening file: {filename}]")
    wordarray = []
    with open(filename, "r") as wordfile:
        for line in wordfile:
            addword = parseline(line)
            if addword:
                wordarray.append(addword)

    endround = time.time() + roundtime

    while wordarray:
        print("\n\n\n\n")
        nextindex = random.randint(0, len(wordarray) - 1)
        nextword = wordarray.pop(nextindex)
        print(nextword)
        print("=" * len(nextword))

        savename = input("Type a name to save, or press enter for next word: ")
        if savename:
            savegame(savename)

        print(f"Time left: {int(endround - time.time())}")
        if time.time() > endround:
            pauseround()
            endround = time.time() + roundtime

    print("[GAME OVER] No more words in the list.")

############
##  GAME  ##
############

roundtime = 60.0 * 4  # default 4 minutes
wordlist_directories = ["words", "saves", "completed"]
saves_directory = wordlist_directories[1]

sound_endround = os.path.join("sounds", "redalert.wav")
rulesfile = "rules.txt"

printrules(rulesfile)

print("Press enter to use defaults:")
print(f"    Default round length: {roundtime}")
try:
    roundtime = float(input("Set round length: "))
except ValueError:
    print("Using defaults then!")

filelist = []
for worddir in wordlist_directories:
    if os.path.isdir(worddir):
        filelist += [os.path.join(worddir, x) for x in os.listdir(worddir) if os.path.isfile(os.path.join(worddir, x))]

if not filelist:
    print("[Error] No word files found. Exiting.")
    sys.exit(1)

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

playround(filename, roundtime)
input("Press enter to quit: ")
