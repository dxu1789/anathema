import os
import sys
import random

filelist = os.listdir(".")
thisfile = sys.argv[0].split("\\")[-1]
filelist.remove(thisfile)

print filelist
# make sure the files are .txt files
# create a menu to select which text file to use

for filename in filelist:
    print "[Opening file: %s]" % (filename)
    
    wordfile = open(filename)
    wordarray = []
    for line in wordfile:
        parsedline = line.replace("\n", "")
        wordarray.append(parsedline)
    wordfile.close()

    while len(wordarray) > 0:
        print "\n\n\n\n"
        raw_input("Press Enter to get next word: ")
        nextindex = random.randint(0, len(wordarray) - 1)
        nextword = wordarray.pop(nextindex)
        print nextword

print
print "[No more words in the list]"
print


