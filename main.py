import os
import time
import Reader
from time import gmtime, strftime

'''

VIEW -  Interacts with Reader.py (model)

'''

#Setting our clearline for our console
CLEAR = "cls" if os.name == "nt" else "clear"
RED = "\033[1;31m" #Formatting options
RESET = "\033[0;0m" #Formatting options
os.system(CLEAR) #Clearing unnecessary text

while True:
    try:
        WPM = int(input("WPM?"))
        if(WPM > 0):
            break
        else:
            print("Please enter a number above 0")
    except:
       print("Please enter a number")


#Creating our reader object
r = Reader.Reader(WPM, CLEAR)
print("Starting ...")
time.sleep(1)
os.system(CLEAR)
#Loading our text sources

while True:    
    filePath = input("Enter folder you want to read\n")
    fileLocations = r.openFolder(filePath)
    if fileLocations is False:
        print("Invalid Folder address. Try again")
        continue #Continuing if we break our address
    break #Turning off our loop
sources = r.loadSources(fileLocations)

# Counting the user in
print("Starting program in 3")
print("\n\n\n\n" + " " * 12 + RED + "X" + RESET + "<----- Look here") 
time.sleep(1)
os.system(CLEAR)
print("Starting program in 2")
print("\n\n\n\n" + " " * 12 + RED + "X" + RESET + "<----- Look here") 
time.sleep(1)
os.system(CLEAR)
print("Starting program in 1")
print("\n\n\n\n" + " " * 12 + RED + "X" + RESET + "<----- Look here")
time.sleep(1)
os.system(CLEAR)

readSpeed = r.getReadSpeed()
r.setStartTime()

for file in fileLocations:
    (splitPath, totalWords) = r.parseFiles(file, sources) #Breaking view convention
    print("\n\n\n\n\n" + " "*12 + RED + "N" + RESET + "ext Source: " + splitPath)
    time.sleep(2)
    os.system(CLEAR)
    count = 0

    for paragraph in sources[file]:
        for word in paragraph.split(" "):
            formattedWord = ""
            (centerPos, sleepModifier) = r.read(file, word)
            # We get an index out of bounds error with words that are 1 letter because of this +1 \/
            if(word[centerPos+1:len(word)]):
                formattedWord = word[0:centerPos] + RED + word[centerPos] + RESET + word[centerPos+1:len(word)]
            else: # Just printing the word
                formattedWord = RED + word + RESET
            print("Origin: " + splitPath) #Keep in mind you'll want to track slide/file origin here
            print("\n\n\n\n" + " "*(12 - centerPos) + formattedWord)
            print("\n\n\n\n")
            print(str(count) + " / " + str(totalWords))
            count = count + 1
            time.sleep(readSpeed * sleepModifier) #Waiting changes depending on context
            os.system(CLEAR)
                
startTime = r.getStartTime() # This breaks the MVC I have going on, but 
elapsedTime = r.getElapsedTime(startTime)

print("Done")
print("Time Started: " + startTime)
print("Time Reading: " + elapsedTime)
print("Time Ended: " + strftime("%H:%M:%S", gmtime()))
print("Total Words Read: " + str(r.getTotalWords()))
print("Read speed: " + str(r.getTrueWPM(elapsedTime)) + "WPM")

