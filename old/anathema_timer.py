import os
import random
import sys
import time


filelist = os.listdir(".")
thisfile = sys.argv[0].split("\\")[-1]
filelist.remove(thisfile)

# make sure the files are .txt files
# create a menu to select which text file to use

def countdown(n):
    for i in range(n, 0, -1):
        print str(i) + " ",
        time.sleep(1)
    print


for filename in filelist:
    if filename.split(".")[-1] != "txt":
        continue

    print "============="
    print "Opening file: %s" % (filename)
    print "============="
    
    wordfile = open(filename)
    wordarray = []
    for line in wordfile:
        parsedline = line.replace("\n", "")
        wordarray.append(parsedline)
    wordfile.close()


    roundlength = 30
    wordinterval = 15
    while len(wordarray) > 0:
        raw_input("Press Enter to start round: ")

        # begin round
        roundstart = time.time()
        
        while (time.time() - roundstart) < roundlength:
            print "\n\n\n\n"
            nextindex = random.randint(0, len(wordarray) - 1)
            nextword = wordarray.pop(nextindex)
            print nextword
            countdown(wordinterval)

        print
        print
        print "----- ROUND OVER -----"



print
print "=============="
print "No more words!"
print "=============="
print


