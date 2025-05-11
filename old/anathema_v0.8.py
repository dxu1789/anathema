#!/usr/bin/python

"""
anathema: a word guessing game
by Kevin Qi

0.9: cross-platform issues: adding os.path.join, uses winsound only for windows
0.8: word folders, parsing
0.7: reverted to non-roundtimed game
0.6: added saved games
0.5: global variables in getword
0.4: added round lengths
0.3: using KeyboardInterrupt to skip timer

"""

IS_WINDOWS = (os.name == "nt")

import os
import random
import sys
import time
if IS_WINDOWS:
    import winsound

#################
##  FUNCTIONS  ##
#################

def printrules(rules):
    f = open(rules)
    print f.read()
    f.close()

def parseline(line):
    """ All-purpose parsing routine.
        Returns empty string if line has no word. """    
    parsedline = line.strip().split()
    if len(parsedline) > 0:
        return line.strip() # parsedline #parsedline[0]
    return ""

def playsound(soundfile):
    if IS_WINDOWS:
        winsound.PlaySound(soundfile, winsound.SND_FILENAME)

def pauseround():
    playsound(sound_endround)
    print "\n\n\n\n"
    raw_input("[ROUND OVER] Press enter to continue.")

def savegame(savename):
    global wordarray
    if len(savename) <= 0:
        print "[Error] Save name given is empty."
        return
    try:
        savetarget = os.path.join(saves_directory, savename + ".txt")
        print "[Saving] " + savetarget
        f = open(savetarget, "w")
        for s in wordarray:
            f.write(s + "\n")
        print "[Game saved]"
    except IOError:
        print "You have failed at typing a name."

def playround(filename, roundtime):
    global wordarray
    global endround

    # add words from filename to wordarray
    print "[Opening file: %s]" % (filename)
    wordarray = []
    wordfile = open(filename)
    for line in wordfile:
        addword = parseline(line)
        if len(addword) > 0:
            wordarray.append(addword)
    wordfile.close()
    
    def getword():
        global wordarray
        global endround
        if len(wordarray) > 0:
            print "\n\n\n\n"
            nextindex = random.randint(0, len(wordarray) - 1)
            nextword = wordarray.pop(nextindex)
            print nextword
            print "".join(["=" for i in nextword])

            savename = raw_input("Type a name to save, or press enter for next word: ")
            if len(savename) > 0:
                savegame(savename)

            # DEBUG
            print "Time left: %d" % (endround - time.time())
            if time.time() > endround:
                pauseround()
                endround = time.time() + roundtime
            getword()
                    
        else:
            print "[GAME OVER] No more words in the list."
            return
            
    # begin round
    endround = time.time() + roundtime  
    getword()
    return

############
##  GAME  ##
############

# parameters
roundtime = 60.0 * 4
wordlist_directories = ["words", "saves", "completed"]
saves_directory = wordlist_directories[1]

sound_endround = os.path.join("sounds", "button.wav")  # "redalert.wav"
rulesfile = "rules.txt"

# display rules
printrules(rulesfile)

# change round timings
print
try:
    print "Press enter to use defaults:"
    print "    Default round length: " + str(roundtime)
    roundtime = float(raw_input("Set round length: "))
except ValueError:
    print "Using defaults then!"
print

# choose word list
filelist = []
for worddir in wordlist_directories:
    filelist += [os.path.join(worddir, x) for x in os.listdir(worddir)]

for i in range(len(filelist)):
    print "[%2d]  %s" % (i, filelist[i])
print

filename = ""
while True:
    try:
        filenumber = int(raw_input("Enter index of file to open: "))
        if filenumber in range(len(filelist)):
            filename = filelist[filenumber]
            break
        else:
            print "[index out of range]"
    except ValueError:
        print "[input was not a number]"

# begin a game
playround(filename, roundtime)
raw_input("Press enter to quit: ")
