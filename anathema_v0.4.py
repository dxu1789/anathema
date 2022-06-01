#!/usr/bin/python

"""
anathema: a word guessing game

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

def playround(filename, guesstime, roundtime):
    print "[Opening file: %s]" % (filename)
    wordfile = open(filename)
    wordarray = []
    for line in wordfile:
        wordarray.append(parseline(line))        
    wordfile.close()

    endround = time.time() + roundtime

    def getword(array, input_endround):
        try:
            playsound(sound_guess)
            print "\n\n\n\n"
            if len(array) > 0:
                # display a word
                nextindex = random.randint(0, len(array) - 1)
                print array.pop(nextindex)

                print "Press [ctrl+c] to skip to next word."
                endguess = time.time() + guesstime

                while time.time() < endguess:
                    print int(round(endguess - time.time())), 
                    time.sleep(1)

                    if time.time() > input_endround:
                        playsound(sound_round)
                        print "\n\n\n\n"
                        raw_input("[ROUND OVER] Press Enter to continue.")
                        input_endround = time.time() + roundtime
                        break
                        # TODO: press something else to save progress and quit

                getword(array, input_endround)
                
            else:
                print "[GAME OVER] No more words in the list."
                return
            
        except KeyboardInterrupt:
            getword(array, input_endround)
            
    getword(wordarray, endround)
    return

############
##  GAME  ##
############

# parameters
guesstime = 20.0
roundtime = 60.0 * 3
rulesfile = "anathema_rules.txt"

sound_guess = "sounds\\redalert.wav"
sound_round = "sounds\\button.wav"

# display rules
printrules(rulesfile)

# change round timings
print
try:
    guesstime = float(raw_input("Enter word guess length: "))
    roundtime = float(raw_input("Enter round length: "))
except ValueError:
    print "Using default guess length: %f, default round length: %f" % (guesstime, roundtime)
print

# choose word list
wordlist_directory = "words"
filelist = os.listdir(wordlist_directory)
print "[Opening directory: %s]" % (wordlist_directory)

for i in range(len(filelist)):
    print "[%s]  %s" % (i, filelist[i])
print

filename = wordlist_directory + "\\"
while True:
    try:
        filenumber = int(raw_input("Enter index of file to open: "))
        if filenumber in range(len(filelist)):
            filename += filelist[filenumber]
            break
        else:
            print "[index out of range]"
    except ValueError:
        print "[input was not a number]"

# begin a game
playround(filename, guesstime, roundtime)
raw_input("Press [enter] to quit: ")
