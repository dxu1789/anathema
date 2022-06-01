#!/usr/bin/python

"""
anathema: a word guessing game
by Kevin Qi

0.7: reverted to non-roundtimed game
0.6: added saved games
0.5: global variables in getword
0.4: added round lengths
0.3: using KeyboardInterrupt to skip timer

"""

import os
import random
import sys
import time
import winsound     # not cross-platform?

#################
##  FUNCTIONS  ##
#################

def printrules(rules):
    f = open(rules)
    print f.read()
    f.close()

def parseline(line):
    """ Custom parsing routine. """
    return line.replace("\n", "")

def playsound(soundfile):
    winsound.PlaySound(soundfile, winsound.SND_FILENAME)

def pauseround():
    global wordarray
    playsound(sound_round)
    print "\n\n\n\n"
    print "[ROUND OVER] Press enter to continue."
    savename = raw_input("Type a save name to save and quit: ")
    
    if len(savename) > 0:
        savetarget = savegame_directory + "\\" + savename + ".txt"
        print "[Saving] " + savetarget
        f = open(savetarget, "w")
        for s in wordarray:
            f.write(s + "\n")
        sys.exit("[Game saved]")

def playround(filename, roundtime):
    global wordarray
    global endround
    
    print "[Opening file: %s]" % (filename)
    wordarray = []
    wordfile = open(filename)
    for line in wordfile:
        wordarray.append(parseline(line))        
    wordfile.close()
    
    def getword():
        global wordarray
        global endround

        if time.time() > endround:
            pauseround()
            endround = time.time() + roundtime

        if len(wordarray) > 0:
            print "\n\n\n\n"
            nextindex = random.randint(0, len(wordarray) - 1)
            nextword = wordarray.pop(nextindex)
            print nextword
            print "".join(["=" for i in nextword])

            raw_input("Press enter for next word: ")
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
roundtime = 60.0 * 3
wordlist_directories = ["saves", "words"]
# savegame_directory = "saves"
# wordlist_directory = "words"

sound_guess = "sounds\\redalert.wav"
sound_round = "sounds\\button.wav"
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
    filelist = [(worddir + "\\" + x) for x in os.listdir(worddir)]
# filelist += [(savegame_directory + "\\" + x) for x in os.listdir(savegame_directory)]

for i in range(len(filelist)):
    print "[%s]  %s" % (i, filelist[i])
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
