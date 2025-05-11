import os

wordlist_directory = "words"
filelist = [(wordlist_directory + "\\" + x) for x in os.listdir(wordlist_directory)]

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

infile = open(filename, "r")
outfile = open(filename + "_PARSED", "w")
for line in infile:
    parsedline = line.strip()
    if len(parsedline) > 0:
        outfile.write(parsedline + "\n")

infile.close()
outfile.close()
