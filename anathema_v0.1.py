# basic, solid version (no timing)

import os
import sys
import random
import winsound

def parseline(line):
    return line.replace("\n", "")

def playround(filename):
    print "[Opening file: %s]" % (filename)
    wordfile = open(filename)
    wordarray = []
    for line in wordfile:
        wordarray.append(parseline(line))        
    wordfile.close()
    
    while len(wordarray) > 0:
        print "\n\n\n\n"
        raw_input("Press Enter to get next word: ")
        nextindex = random.randint(0, len(wordarray) - 1)
        nextword = wordarray.pop(nextindex)
        print nextword
        
    print "[ROUND COMPLETE: no more words in the list]"
    print
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
