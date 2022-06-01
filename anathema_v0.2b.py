# failed threading.Timer() version

import os
import random
import sys
import threading
import winsound

def parseline(line):
    # tokens = line.split()
    # wordarray.append(tokens[0] + " " + tokens[1])
    # parsedline = line.split(":")[0] # chemistry words
    # parsedline = line.split()
    # if (parsedline != "\n"):
    #    wordarray.append(parsedline)

    return line.replace("\n", "")

def playround(filename):
    print "[Opening file: %s]" % (filename)
    wordfile = open(filename)
    wordarray = []
    for line in wordfile:
        wordarray.append(parseline(line))        
    wordfile.close()

    def getword(array):
        print "\n\n\n\n"
        if len(array) > 0:
            # display a word
            nextindex = random.randint(0, len(array) - 1)
            print array.pop(nextindex)

            # display the next word in a time limit
            nextwordtimer = threading.Timer(5.0, getword, [array])  # NOTE: not getword()
            nextwordtimer.start()

            # override the time limit
            raw_input("Press [enter] if word was guessed successfully: ")
            nextwordtimer.cancel()
            getword(array)

        else:
            print "[ROUND COMPLETE: no more words in the list]"
            return
            
    getword(wordarray)
    return

wordlist_directory = "words"
filelist = os.listdir(wordlist_directory)
print "[Opening directory: %s]" % (wordlist_directory)

for i in range(len(filelist)):
    print "[%s]  %s" % (i, filelist[i])

badinput = True
filename = "words\\"
while badinput:
    try:
        filenumber = int(raw_input("Enter index of file to open: "))
        if filenumber in range(len(filelist)):
            filename += filelist[filenumber]
            badinput = False
        else:
            print "[index out of range]"
    except ValueError:
        print "[input was not a number]"


playround(filename)
