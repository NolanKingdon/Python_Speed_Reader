import os 
import time
import glob
from pptx import Presentation
from docx import Document
import PyPDF2 as pypdf2

# NOTE: This is just a quick and dirty tool I made because I needed something to help study.
#       In the future I am going to be redoing this to be better form
#       That means having an actual file structure and MVC approach

def openFolder():
    fileList = []
    filePath = input("Enter folder you want to read\n")
    for file in os.listdir(filePath):
        if filePath[-1] == "\\":
            fileList.append(filePath + file)
        else: 
            fileList.append(filePath + "\\" + file)
    return fileList

def scrapePDF(filePath):
    paragraphs = []
    pdfReader = pypdf2.PdfFileReader(filePath)
    pageNo = pdfReader.getNumPages()
#    print(pdfReader.getPage(0).extractText())

    for i in range(0, pageNo):
        paragraphs += pdfReader.getPage(i).extractText().split("\n")

    return paragraphs


def scrapeTXT(filePath):
    paragraphs = []
    file = open(filePath, 'r')
    unformattedText = file.read();
    paragraphs = unformattedText.split("\n") #Splitting by paragraph
    return paragraphs

def scrapeDOCX(filePath):
    paragraphs = []
    doc = Document(filePath)
    for paragraph in doc.paragraphs:
        paragraphs.append(paragraph.text)
    return paragraphs

def scrapePPTX(filePath):
    paragraphs = []
    pres = Presentation(filePath)
    for slide in pres.slides: #Looking through our slides
        for shape in slide.shapes: #Looking through objects in that slide
            if not shape.has_text_frame: #Seeing if we have any text on that slide
                continue
            #for title in shape.name
            for paragraph in shape.text_frame.paragraphs: #reading all paragraphs on the slide
                paragraphs.append(paragraph.text)
    return paragraphs


def countIn():
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

def read(source, paragraphs):
    for paragraph in paragraphs:
        for word in paragraph.split(" "):
            #Finding the letter roughly one third of the way through the word to center
            centerPos = int(len(word)/3)
            origin = source.split("/") if source[-1] == "/" else source.split("\\")
            #Setting sleep Modifier based on word length or placing in sentence
            sleepModifier = 1 #How long we want to wait on each word        
            if (len(word) > 0): #Ensuring we don't run into issues with blank spaces       
                if(len(word) > 7):
                    sleepModifier = 1.8
                elif(word[-1] in ".,-?!;:"):
                    sleepModifier = 2
                        
                formattedWord = word[0:centerPos] + RED + word[centerPos] + RESET + word[centerPos+1:len(word)] + RESET        
                print("Origin: " + origin[-1]) #Keep in mind you'll want to track slide/file origin here
                print("\n\n\n\n" + " "*(12 - centerPos) + formattedWord)
                print("\n\n\n\nWords per minute:\t~" + str(WPM))
                time.sleep(READ_SPEED * sleepModifier) #Waiting changes depending on context
            else:
                print("Origin: " + origin[-1]) #Keep in mind you'll want to track slide/file origin here
                print("\n\n\n\n")
                print("\n\n\n\nWords per minute:\t~" + str(WPM))
            os.system(CLEAR) #clearing our terminal so we can stay at the top of the window
            

# VARIABLE DECLARATIONS

CLEAR = "cls" if os.name == "nt" else "clear"
READ_SPEED = 0.07 #0.07 is manageable
WPM = round(60 / READ_SPEED) #Seconds in a minute.
#Test paragraph below
testP = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."

RED = "\033[1;31m" #Formatting options
RESET = "\033[0;0m" #Formatting options
BOLD = "\033[1m" #Formatting options
os.system(CLEAR) # Getting all the junk out of the way before we start

#  --- MAIN RUNTIME ---

fileLocations = openFolder()
sources = {}

for file in fileLocations:
    ext = file.split(".")[-1].lower()
#    print(ext)
    print("Reading " + file + "...")
    time.sleep(0.5)
    os.system(CLEAR)
    if (ext == "pptx"):
        sources[file] = scrapePPTX(file)
    if (ext == "docx"):
        sources[file] = scrapeDOCX(file)
    if (ext == "txt"):
        sources[file] = scrapeTXT(file)
    if (ext == "pdf"):
        sources[file] = scrapePDF(file)
print("Starting ...")
time.sleep(1)
countIn()

for file in fileLocations:
    splitPath = file.split("/") if file[-1] == "/" else file.split("\\")
    print("\n\n\n\n\n" + " "*12 + RED + "N" + RESET + "ext Source: " + splitPath[-1])
    time.sleep(2)
    os.system(CLEAR)
    read(file, sources[file])
    os.system(CLEAR)


print("Done")



