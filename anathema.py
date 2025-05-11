#!/usr/bin/python3

import os
import random
import sys
import time

IS_WINDOWS = (os.name == "nt")
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
    if len(parsedline) > 0:
        return line
    return ""

def playsound(soundfile):
    if IS_WINDOWS:
        winsound.PlaySound(soundfile, winsound.SND_FILENAME)
    else:
        os.system(f'afplay "{soundfile}" &')

def pauseround():
    playsound(sound_endround)
    print("\n\n\n\n")
    input("[ROUND OVER] Press enter to continue.")

def savegame(savename):
    global wordarray
    if len(savename) <= 0:
        print("[Error] Save name given is empty.")
        return
    try:
        savetarget = os.path.join(saves_directory, savename + ".txt")
        print(f"[Saving] {savetarget}")
        with open(savetarget, "w") as f:
            for s in wordarray:
                f.write(s + "\n")
        print("[Game saved]")
    except IOError:
        print("You have failed at typing a name.")

def playround(filename, roundtime):
    global wordarray
    global endround

    print(f"[Opening file: {filename}]")
    wordarray = []
    with open(filename, "r") as wordfile:
        for line in wordfile:
            addword = parseline(line)
            if len(addword) > 0:
                wordarray.append(addword)

    def getword():
        global wordarray
        global endround
        if len(wordarray) > 0:
            print("\n\n\n\n")
            nextindex = random.randint(0, len(wordarray) - 1)
            nextword = wordarray.pop(nextindex)
            print(nextword)
            print("".join(["=" for _ in nextword]))

            savename = input("Type a name to save, or press enter for next word: ")
            if len(savename) > 0:
                savegame(savename)

            print(f"Time left: {int(endround - time.time())}")
            if time.time() > endround:
                pauseround()
                endround = time.time() + roundtime
            getword()
        else:
            print("[GAME OVER] No more words in the list.")
            return

    endround = time.time() + roundtime
    getword()

############
##  GAME  ##
############

roundtime = 60.0 * 4
wordlist_directories = ["words", "saves", "completed"]
saves_directory = wordlist_directories[1]

sound_endround = os.path.join("sounds", "button.wav")
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
    filelist += [os.path.join(worddir, x) for x in os.listdir(worddir)]

for i, file in enumerate(filelist):
    print(f"[{i:2d}]  {file}")

filename = ""
while True:
    try:
        filenumber = int(input("Enter index of file to open: "))
        if filenumber in range(len(filelist)):
            filename = filelist[filenumber]
            break
        else:
            print("[index out of range]")
    except ValueError:
        print("[input was not a number]")

playround(filename, roundtime)
input("Press enter to quit: ")