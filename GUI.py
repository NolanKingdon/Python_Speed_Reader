from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QSlider, QProgressBar, QCheckBox
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from Styles import Styles
import sys
import Reader
import time
import threading
import os

'''

    GUI Application.

    Build using PyQt5.

    Uses absolute positioning rather than layouts due to the precise setup of the word reader itself - layouts did not
        appropriately accomodate splitting a word into separate QLabels

    Will be looking into making the modules into separate classes for increased readability and structure
    Will be looking into adding metrics to te end of the read period
    Will be looking into creating an executable and potentially porting this to phones.
    Will be adding single file support

    @author - Nolan Kingdon

'''
class App(QWidget):

    '''
        Class variables

        Set up here due to the fact that pyqt was causing issues if there were initialized normally
    '''
    #Setting up the emit Signals so we can appropriately increment the progress bar
    updated = pyqtSignal(int)
    styles = Styles("normal")
    stylesDict = styles.getStyles()
    '''
        Constructor

        Creates instance variables and initializes the UI

    '''   
    def __init__(self):
        super().__init__()
        self.title = 'Speed Reader'
        self.setWindowIcon(QIcon('icon.png'))        
        # *** Instance Variables
        self.READ = True
        self.DARKMODE = False
        self.reader = Reader.Reader(100, "")
        self.currentFile = ""
        self.paragraphIndex = 0
        self.wordIndex = 0
        self.dir_ = ""
        self.WPM = 300
        self.extras = False
        self.left = 100
        self.top = 100
        self.initUI()

        self.setStyleSheet(self.stylesDict['main'])

    '''
        Initializing the UI

        Calls the create module methods and defines window parameters

    '''
    def initUI(self):
        self.setWindowTitle(self.title) #Assigning the GUI window title
        self.setGeometry(self.left, self.top, 500, 150) #Defining the window size/initial position
        
        self.createTopBar(self.stylesDict["top"])        # Creating the buttons
        self.createWordReader(self.stylesDict["word"])   # Creating the word reader itself
        self.createFloaters(self.stylesDict["float"])    # Creating all floating attributes/labels
        self.createExtras(self.stylesDict["extra"])      # Creating the initially hidden extras


        self.show() #Showing GUI

    # *** GUI Creation Functions ***

    '''
        Creates Top bar module

        Includes the controls and WPM selector

        @TOP_STYLES - String - Defined in Styles.py - styles depending on mode
    '''
    def createTopBar(self, TOP_STYLES):

        #Start button
        self.start = QPushButton('Start', self)
        self.start.setToolTip('Start Speed Reading')
        self.start.move(0, 0)
        self.start.clicked.connect(self.startRead)
        self.start.setEnabled(False) # Initially falsed to prevent starting with no sources loaded

        #Pause Button
        self.pause = QPushButton('Pause', self)
        self.pause.setToolTip('Pause Current Read Stream')
        self.pause.move(75, 0)
        self.pause.clicked.connect(self.toggleRead)
        self.pause.setEnabled(False)
        
        # Reset Button
        self.reset = QPushButton('Reset', self)
        self.reset.setToolTip('Completely Reset the reader')
        self.reset.move(150, 0)
        self.reset.clicked.connect(self.stopRead)

        # Open Folder Button
        self.openFolder = QPushButton('Open Folder', self)
        self.openFolder.setToolTip('Select your folder to read from')
        self.openFolder.move(225, 0)
        self.openFolder.clicked.connect(self.openLocation)
        
        # Words per minute slider
        self.wpmSlider = QSlider(Qt.Horizontal, self)
        self.wpmSlider.setGeometry(300, 0, 200, 30)
        self.wpmSlider.setValue(30) #Our start value
        self.wpmSlider.valueChanged[int].connect(self.changeWPM)

        # Applying styles
        self.setTopStyles(TOP_STYLES)

    '''
        Creates the word reader itself

        Word reader is comprised of three separate labels. There was no way in any of the GUI libraries to just make
        a single letter of the word a different color (As required to focus properly on the word). This was the
        easiest solution. This also mandates we use absolute positioning to get these labels close enough that we can
        make it look like one cohesive word

        @WORD_STYLES - String - Defined in Styles.py - styles depending on mode
    '''
    def createWordReader(self, WORD_STYLES):

        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 60, 460, 30) # lays behind the labels
        self.progress.setMaximum(100)

        # Three labels we split the word into
        self.w1 = QLabel("Wo", self)
        self.w2 = QLabel("r", self)
        self.w3 = QLabel("ds", self)

        # Configuring labels individually
        self.w1.move(20, 60)
        self.w1.setFont(QFont("Courier", 20)) # Courier is monospace - this is !important!
        self.w1.setAlignment(Qt.AlignRight)
        self.w1.resize(200, 30)

        self.w2.setStyleSheet("color: #FF0000;")
        self.w2.move(220, 60)
        self.w2.setFont(QFont("Courier", 20))
        self.w2.setAlignment(Qt.AlignCenter)
        self.w2.setObjectName("red-letter") # The red letter gets special styling, so it gets an object name

        self.w3.move(235, 60)
        self.w3.setFont(QFont("Courier", 20))
        self.w3.resize(230, 30)
        self.w3.setAlignment(Qt.AlignLeft)

        # Assigning spreadsheets to the related elements
        self.setWordStyles(WORD_STYLES)

    '''
        Creates Optional Extras

        creates modules that give unnecessary information on the document/paragraph being read

        TODO - Implement the metrics from the ConsoleUI into this to display when the file is done reading **

        @EXTRA_STYLES - String - Defined in Styles.py - styles depending on mode
    '''        
    def createExtras(self, EXTRA_STYLES):
        # Current Paragraph section
        self.paragraph = QLabel("Paragraph", self)
        self.paragraph.move(20, 180)
        self.paragraph.resize(460, 600)
        self.paragraph.setAlignment(Qt.AlignCenter) # Center aligned
        self.paragraph.setFont(QFont("Calibri", 15))
        self.paragraph.setWordWrap(True)
        self.paragraph.setObjectName("summary-paragraph")

        # Current file being read
        self.currentFile = QLabel("Current File", self)
        self.currentFile.move(20, 150)
        self.currentFile.resize(480, 20)
        self.currentFile.setFont(QFont("Calibri", 15))
        self.currentFile.setObjectName("current-file")

        # Setting stylesheets
        self.setExtraStyles(EXTRA_STYLES)

        # Starting these hidden to keep UX good - sleek start and THEN opt into all the extras
        self.paragraph.hide()
        self.currentFile.hide()

    '''
        Creates Floating modules

        Anything that is a label or checkbox that does not fit into one specific section is here

        @FLOAT_STYLES - String - Defined in Styles.py - styles depending on mode
    '''
    def createFloaters(self, FLOAT_STYLES):
        # Defines extra box.
        self.extraBox = QCheckBox("Show Detailed View", self)
        self.extraBox.move(20,120)
        self.extraBox.clicked.connect(self.handleCheck) # Unhides the Paragraph and title section

        # Toggles dark mode
        self.darkMode = QCheckBox("Dark Mode", self)
        self.darkMode.move(400, 120)
        self.darkMode.clicked.connect(self.toggleDarkmode)

        # WPM Label - Updates on slider use. Initializes at 300
        self.wpmLabel = QLabel(str(self.WPM) + "WPM", self)
        self.wpmLabel.move(375, 30)
        self.wpmLabel.setObjectName("wpm")

        # Applying stylesheets
        self.setFloaterStyles(FLOAT_STYLES)

    '''
        Sets Styles for topbar elements

        @TOP_STYLES - String - Defined in Styles.py - styles depending on mode
    '''
    def setTopStyles(self, TOP_STYLES):
        self.openFolder.setStyleSheet(TOP_STYLES)
        self.wpmSlider.setStyleSheet(TOP_STYLES)
        self.reset.setStyleSheet(TOP_STYLES)
        self.pause.setStyleSheet(TOP_STYLES)
        self.start.setStyleSheet(TOP_STYLES)

    '''
        Sets Styles for word reader elements

        @WORD_STYLES - String - Defined in Styles.py - styles depending on mode
    '''        
    def setWordStyles(self, WORD_STYLES):
        self.w1.setStyleSheet(WORD_STYLES)
        self.w2.setStyleSheet(WORD_STYLES)
        self.w3.setStyleSheet(WORD_STYLES)
        self.progress.setStyleSheet(WORD_STYLES)
        
    '''
        Sets Styles for extra elements

        @EXTRA_STYLES - String - Defined in Styles.py - styles depending on mode
    '''    
    def setExtraStyles(self, EXTRA_STYLES):
        self.paragraph.setStyleSheet(EXTRA_STYLES)
        self.currentFile.setStyleSheet(EXTRA_STYLES)
        
    '''
        Sets Styles for floating elements

        @FLOAT_STYLES - String - Defined in Styles.py - styles depending on mode
    '''
    def setFloaterStyles(self, FLOAT_STYLES):
        self.extraBox.setStyleSheet(FLOAT_STYLES)
        self.darkMode.setStyleSheet(FLOAT_STYLES)
        self.wpmLabel.setStyleSheet(FLOAT_STYLES)

    '''
        Toggles darkmode - Slots with the darkmode checkbox
    '''
    @pyqtSlot()
    def toggleDarkmode(self):
        # Inverting our dark mode
        self.DARKMODE = not self.DARKMODE

        # Re-generating the style sheet
        if self.DARKMODE:
            self.styles.setStyles("dark")
            self.stylesDict = self.styles.getStyles()
        elif not self.DARKMODE:
            self.styles.setStyles("normal")
            self.stylesDict = self.styles.getStyles()
            
        #Re-applying our styles to all affected groups          
        self.setStyleSheet(self.stylesDict['main'])
        self.setWordStyles(self.stylesDict["word"])
        self.setTopStyles(self.stylesDict["top"])
        self.setFloaterStyles(self.stylesDict["float"])
        self.setExtraStyles(self.stylesDict["extra"])

    '''
        Toggles extra panes - associated with the "Show Detailed View" checkbox
    '''
    @pyqtSlot()
    def handleCheck(self):
        self.extras = not self.extras

        #Unhiding/hiding the hidden elements
        if not self.extras:
            self.paragraph.hide()
            self.currentFile.hide()
            self.resize(500, 150)
        else:
            self.paragraph.show()
            self.currentFile.show()
            self.resize(500, 800)
    '''
        Changes the WPM word speed. Associated with the slidebar
    '''
    @pyqtSlot()
    def changeWPM(self):
        # Making sure we can't have 0 WPM
        value = self.wpmSlider.value() if self.wpmSlider.value() > 0 else 1
        self.WPM = value*10 # Values are stored 1-100, but WPM needs to be fast: 100-1000
        self.wpmLabel.setText(str(self.WPM)+"WPM")

    '''
        Opens a folder location. Associated with "Open Folder" button

        Will expand this in the future to take a parameter to decide if it's going to open a sole file instead.
    '''
    @pyqtSlot()
    def openLocation(self):
        self.dir_ = QFileDialog.getExistingDirectory(None, 'Select a Folder:', "Documents", QFileDialog.ShowDirsOnly)
        self.start.setEnabled(True)

    '''
        Toggles the read - associated with the pause button

        Currently only pauses the read thread
    '''
    @pyqtSlot()
    def toggleRead(self):
        if self.READ:
            self.pause.setEnabled(False) # Pausing twice would cause issues
            self.start.setEnabled(True) # Allows the read to begin again
            self.READ = not self.READ

    '''
        Starts the read process - associated with start button
    '''
    @pyqtSlot()
    def startRead(self):
        self.start.setEnabled(False) # Starting the read process twice causes problems
        self.pause.setEnabled(True) # Allows us to pause the stream
        self.READ = True # Indicates we are now reading
        inp = self.dir_ #Throw an alert if nothing is here - TODO *** Currently causes an error
        fileLocations = "" #Initializing our filepaths

        if len(inp.split(".")) == 2: #The end of the location has an extension and is a file
            pass #Will handle the file read here in the future        
        elif len(inp.split(".")) == 1: #This is a folder not a file
            if inp is not "": # Making 100% sure something is in there
                fileLocations = self.reader.openFolder(inp) # Error handle here too
        
        sources = self.reader.loadSources(fileLocations) # Processing sources
        
        # Creating a thread - necessary to allow for the read to be inturrupted
        x = threading.Thread(target=self.read, args=(str(self.WPM), fileLocations, sources))
        x.start() # Start thread

    """
        Displays cool end metrics tracked by the reader object to the paragraph screen
    """
    def endMetrics(self):
        wordsRead = self.reader.getTotalWords()
        startTime = self.reader.getStartTime()
        elapsedTime = self.reader.getElapsedTime(startTime)
        trueWPM = self.reader.getTrueWPM(elapsedTime)
        # *** Adding the metric information to the paragraph area

        self.paragraph.setText("Total Words Read: " + str(wordsRead) + "\nStart Time: " + str(startTime) + "\nRead Time: " +
                               str(elapsedTime) + " seconds\n Actual Words Per Minute: " + str(trueWPM))
        
        self.reader.reset() # Resetting the reader because we're done.

    '''
        The Emit handler for incrementing the progress bar

        PyQt5 does not allow anything but the main thread to call repaint(). This is used by Emits to solve the
        problem
    '''
    def handleTrigger(self, i):
        self.progress.setValue(i)

    '''
        Reading the file

        Loops the current file and calls the Reader to parse it.
        Splits the word appropriately and writes to our three labels
    '''
    def read(self, WPM, fileLocations, sources):
        self.updated.connect(self.handleTrigger) # Connecting to our emit handler
        self.reader.setStartTime() # Tracking when we actually start reading
        self.reader.setReadSpeed(int(WPM)) #Setting our sleep value
        readSpeed = self.reader.getReadSpeed() #Getting our sleep value
        

        '''
            Note - There's a lot of work going on here that's not in the reader. Work on making the reader hold...

                - Current File
                - Current Word
                - Current Paragraph

            to be more consistent with MVC
        '''
        try:
            while(self.READ):
                for file in fileLocations:
                    # Splitting the current file text to just be the file name and no directories
                    self.currentFile.setText(file.split("\\")[-1]) #This may give issues in UNIX systems - verify
                    # If we're poaused, we break
                    if not self.READ: break
                    # Other wise, if We're in our first read, we will need to initialize our count, readWords, and paths
                    if self.paragraphIndex == 0 and self.wordIndex == 0: #If this is our first read and not an unpause
                        count = 0
                        (splitPath, self.totalWords) = self.reader.parseFiles(file, sources)
                        self.readWords = 0
                    # Looking through our unread paragraphs
                    while self.paragraphIndex < len(sources[file]): # Using a while loop so we can pick up at the last index if paused
                        #Setting the extra's paragraph text
                        self.paragraph.setText(sources[file][self.paragraphIndex])
                        
                        #Looking through our unread words
                        while self.wordIndex < len(sources[file][self.paragraphIndex].split(" ")):
                            #Emitting the progress bar update to the handler so only GUI touches it
                            self.updated.emit((self.readWords/self.totalWords)*100)
                            word_ = "" # Holder for the current word
                            sleepModifier = 0 # Default sleep modifier - for blanks it wont wait at all
                            #Making sure we have a word to work with
                            if(sources[file][self.paragraphIndex].split(" ")[self.wordIndex]): # If there is a word there
                                # assign that word to our placeholder
                                word_ = sources[file][self.paragraphIndex].split(" ")[self.wordIndex]
                                # Use our reader object to read the word from the file
                                (centerPos, sleepModifier) = self.reader.read(file, word_)
                                #Splitting our word into three seperate text boxes for desired effect                        
                                self.w1.setText(word_[0:centerPos])
                                self.w2.setText(word_[centerPos])
                                self.w3.setText(word_[centerPos+1:len(word_)])
                            #
                            #(centerPos, sleepModifier) = self.reader.read(file, word_)
                            self.readWords += 1 #Our words for tracking overall progress in the file
                            self.wordIndex += 1 #Our words for tracking where we are should we want to pause and resume
                            time.sleep(readSpeed * sleepModifier) # Keeping the word displayed for this long
                            
                            if not self.READ: break # Breaking if the read is paused
                        if not self.READ: break # Breaking if the read is paused
                        self.wordIndex = 0 # If we complete the paragraph, reset our wordIndex back to the first one
                        self.paragraphIndex +=1 # Moving on to the next paraghraph
                    if self.READ: #Only want to reset this once we're still reading, but done the source
                        self.paragraphIndex = 0
                        self.wordIndex = 0
                    else:
                        break
                # *** Done reading all the files
                if not self.READ : break # If we are pausing, we don't want to do any of the below
                self.updated.emit(100) # Updating out the final notch to the percent bar
                self.READ = False
                self.endMetrics() # Printing cool metrics to the paragraph section
                self.reader.clearLastWord() # Clearing the last stored word in our reader object
        except Exception as e:
            print("Something went wrong!\n" + str(e))

    '''
        Stopping the read - associated with the restart button.

        Clears out all the stored information and moves it back to defaults
    '''
    @pyqtSlot()
    def stopRead(self):
        self.currentFile.setText("Current File")
        self.start.setEnabled(True)
        self.pause.setEnabled(False)
        self.READ = False
        self.paragraph.setText("Paragraph")
        self.paragraphIndex = 0
        self.wordIndex = 0
        self.w1.setText("Wo")
        self.w2.setText("r")
        self.w3.setText("ds")
        self.progress.setValue(0)
        self.reader.reset() # Completely resetting our reader as well.
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



