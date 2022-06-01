# using KeyboardInterrupt to skip timer

import os
import random
import sys
import threading
import time
import winsound

###############
#  FUNCTIONS  #
###############

def printrules():
    print """
    Rules of anathema
    =================
    Explainer:
        [+1] successful explanation
        
    Guesser:
        [+1] correct guess
    """

def parseline(line):
    """ Custom parsing routine. """
    
    return line.replace("\n", "")

def playsound():
    winsound.PlaySound("sounds\\alarm.wav", winsound.SND_FILENAME)

def playround(filename):
    print "[Opening file: %s]" % (filename)
    wordfile = open(filename)
    wordarray = []
    for line in wordfile:
        wordarray.append(parseline(line))        
    wordfile.close()

    def getword(array):
        try:
            playsound()
            print "\n\n\n\n"
            if len(array) > 0:
                # display a word
                nextindex = random.randint(0, len(array) - 1)
                print array.pop(nextindex)

                print "Press [ctrl+c] to skip to next word."
                begin = time.time()
                offset = 10.0
                end = begin + offset
                while time.time() < end:
                    print round(end - time.time()), 
                    time.sleep(1)

                getword(array)
                
            else:
                print "[ROUND COMPLETE: no more words in the list]"
                return
            
        except KeyboardInterrupt:
            getword(array)
            
    getword(wordarray)
    return

##########
#  GAME  #
##########

printrules()

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

playround(filename)
raw_input("Press [enter] to quit: ")
