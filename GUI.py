from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QSlider, QProgressBar, QCheckBox
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from Styles import Styles
import sys
import Reader
import time
import threading
import os

class App(QWidget):

    #Setting up the emit Signals so we can appropriately increment the progress bar
    updated = pyqtSignal(int)
    styles = Styles("normal")
    stylesDict = styles.getStyles()
    
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
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, 500, 150)
        
        self.createTopBar(self.stylesDict["top"])        # Creating the buttons
        self.createWordReader(self.stylesDict["word"])   # Creating the word reader itself
        self.createFloaters(self.stylesDict["float"])    # Creating all floating attributes/labels
        self.createExtras(self.stylesDict["extra"])      # Creating the initially hidden extras


        self.show()

    #GUI Creation Functions

    def createTopBar(self, TOP_STYLES):
        self.start = QPushButton('Start', self)
        self.start.setToolTip('Start Speed Reading')
        self.start.move(0, 0)
        self.start.clicked.connect(self.startRead)
        
        
        self.pause = QPushButton('Pause', self)
        self.pause.setToolTip('Pause Current Read Stream')
        self.pause.move(75, 0)
        self.pause.clicked.connect(self.toggleRead)
        self.pause.setEnabled(False)
        

        self.reset = QPushButton('Reset', self)
        self.reset.setToolTip('Completely Reset the reader')
        self.reset.move(150, 0)
        self.reset.clicked.connect(self.stopRead)
        
        
        self.openFolder = QPushButton('Open Folder', self)
        self.openFolder.setToolTip('Select your folder to read from')
        self.openFolder.move(225, 0)
        self.openFolder.clicked.connect(self.openLocation)
        

        self.wpmSlider = QSlider(Qt.Horizontal, self)
        self.wpmSlider.setGeometry(300, 0, 200, 30)
        self.wpmSlider.setValue(30) #Our start value
        self.wpmSlider.valueChanged[int].connect(self.changeWPM)

        self.setTopStyles(TOP_STYLES)

    def createWordReader(self, WORD_STYLES):
        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 60, 460, 30)
        self.progress.setMaximum(100)
        
        #self.progress.setStyleSheet("background-color: #FFFFFF")

        self.w1 = QLabel("Wo", self)
        self.w2 = QLabel("r", self)
        self.w3 = QLabel("ds", self)
        
        
        #self.w1.setStyleSheet("background-color: #FFFFFF");
        self.w1.move(20, 60)
        self.w1.setFont(QFont("Courier", 20))
        self.w1.setAlignment(Qt.AlignRight)
        self.w1.resize(200, 30)

        self.w2.setStyleSheet("color: #FF0000;")# background-color:#FFFFFF;")
        self.w2.move(220, 60)
        self.w2.setFont(QFont("Courier", 20))
        self.w2.setAlignment(Qt.AlignCenter)
        self.w2.setObjectName("red-letter")

        self.w3.move(235, 60)
        self.w3.setFont(QFont("Courier", 20))
        self.w3.resize(230, 30)
        self.w3.setAlignment(Qt.AlignLeft)


        self.setWordStyles(WORD_STYLES)
        
    def createExtras(self, EXTRA_STYLES):
        self.paragraph = QLabel("Paragraph", self)
        self.paragraph.move(20, 180)
        self.paragraph.resize(460, 600)
        self.paragraph.setAlignment(Qt.AlignCenter)
        self.paragraph.setFont(QFont("Calibri", 15))
        self.paragraph.setWordWrap(True)
        self.paragraph.setObjectName("summary-paragraph")

        self.currentFile = QLabel("Current File", self)
        self.currentFile.move(20, 150)
        self.currentFile.resize(300, 20)
        self.currentFile.setFont(QFont("Calibri", 15))
        self.currentFile.setObjectName("current-file")

        self.setExtraStyles(EXTRA_STYLES)
        
        self.paragraph.hide()
        self.currentFile.hide()

    def createFloaters(self, FLOAT_STYLES):
        self.extraBox = QCheckBox("Show Detailed View", self)
        self.extraBox.move(20,120)
        self.extraBox.clicked.connect(self.handleCheck)
        
        self.darkMode = QCheckBox("Dark Mode", self)
        self.darkMode.move(400, 120)
        self.darkMode.clicked.connect(self.toggleDarkmode)

        self.wpmLabel = QLabel(str(self.WPM) + "WPM", self)
        self.wpmLabel.move(375, 30)  

        self.setFloaterStyles(FLOAT_STYLES)

    def setTopStyles(self, TOP_STYLES):
        self.openFolder.setStyleSheet(TOP_STYLES)
        self.wpmSlider.setStyleSheet(TOP_STYLES)
        self.reset.setStyleSheet(TOP_STYLES)
        self.pause.setStyleSheet(TOP_STYLES)
        self.start.setStyleSheet(TOP_STYLES)
        
    def setWordStyles(self, WORD_STYLES):
        self.w1.setStyleSheet(WORD_STYLES)
        self.w2.setStyleSheet(WORD_STYLES)
        self.w3.setStyleSheet(WORD_STYLES)
        self.progress.setStyleSheet(WORD_STYLES)
    
    def setExtraStyles(self, EXTRA_STYLES):
        self.paragraph.setStyleSheet(EXTRA_STYLES)
        self.currentFile.setStyleSheet(EXTRA_STYLES)

    def setFloaterStyles(self, FLOAT_STYLES):
        pass

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
        self.setExtraStyles(self.stylesDict["extra"])
        
    @pyqtSlot()
    
    def handleCheck(self):
        self.extras = not self.extras
        
        if not self.extras:
            self.paragraph.hide()
            self.currentFile.hide()
            self.resize(500, 150)
        else:
            self.paragraph.show()
            self.currentFile.show()
            self.resize(500, 800)
    
    @pyqtSlot()
    def changeWPM(self):
        value = self.wpmSlider.value() if self.wpmSlider.value() > 0 else 1
        self.WPM = value*10
        self.wpmLabel.setText(str(self.WPM)+"WPM")

    @pyqtSlot()
    def openLocation(self):
        self.dir_ = QFileDialog.getExistingDirectory(None, 'Select a Folder:', "Documents", QFileDialog.ShowDirsOnly)

    @pyqtSlot()
    def toggleRead(self):
        if self.READ:
            self.pause.setEnabled(False)
            self.start.setEnabled(True)
            self.READ = not self.READ

    @pyqtSlot()
    def startRead(self):
        self.start.setEnabled(False)
        self.pause.setEnabled(True)
        self.READ = True
        inp = self.dir_ #Throw an alert if nothing is here - TODO
        fileLocations = "" #Initializing our filepaths

        if len(inp.split(".")) == 2: #The end of the location has an extension and is a file
            pass #Will handle the file read here in the future        
        elif len(inp.split(".")) == 1: #This is a folder not a file
            fileLocations = self.reader.openFolder(inp) # Error handle here too
        sources = self.reader.loadSources(fileLocations)
        x = threading.Thread(target=self.read, args=(str(self.WPM), fileLocations, sources))
        x.start()

    def handleTrigger(self, i):
        self.progress.setValue(i)

    def read(self, WPM, fileLocations, sources):
        self.updated.connect(self.handleTrigger)
        
        self.reader.setReadSpeed(int(WPM)) #Setting our sleep value
        readSpeed = self.reader.getReadSpeed() #Getting our sleep value    
        print(self.paragraphIndex)

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
                    
                    self.currentFile.setText(file.split("\\")[-1]) #This may give issues in UNIX systems - verify
                    print("start of file loop")
                    if not self.READ: break
                    if self.paragraphIndex == 0 and self.wordIndex == 0: #If this is our first read and not an unpause
                        count = 0
                        (splitPath, self.totalWords) = self.reader.parseFiles(file, sources)
                        self.readWords = 0
                    print("end of file loop")
                    # Looking through our unread paragraphs
                    while self.paragraphIndex < len(sources[file]):
                        print("start of paragraph loop")
                        self.paragraph.setText(sources[file][self.paragraphIndex])
                        
                        #Looking through our unread words
                        while self.wordIndex < len(sources[file][self.paragraphIndex].split(" ")):

                            #Emitting the progress bar update to the handler so only GUI touches it
                            self.updated.emit((self.readWords/self.totalWords)*100)
                            #self.progress.setValue((self.wordIndex/totalWords)*100)
                            print("start of word loop")
                            word_ = ""
                            #Making sure we have a word to work with
                            print("Checking length")

                            if(sources[file][self.paragraphIndex].split(" ")[self.wordIndex]):
                                word_ = sources[file][self.paragraphIndex].split(" ")[self.wordIndex]
                                (centerPos, sleepModifier) = self.reader.read(file, word_)
                                #Splitting our word into three seperate text boxes for desired effect                        
                                self.w1.setText(word_[0:centerPos])
                                self.w2.setText(word_[centerPos])
                                self.w3.setText(word_[centerPos+1:len(word_)])
                            
                            (centerPos, sleepModifier) = self.reader.read(file, word_)
                            self.readWords += 1 #Our words for tracking overall progress in the file
                            self.wordIndex += 1 #Our words for tracking where we are should we want to pause and resume
                            time.sleep(readSpeed * sleepModifier)
                            if not self.READ: break
                        if not self.READ: break
                        self.wordIndex = 0
                        self.paragraphIndex +=1
                        print("Next paragraph.")
                    if self.READ: #Only want to reset this once we're still reading, but done the source
                        self.paragraphIndex = 0
                        self.wordIndex = 0
                    else:
                        break
                # *** Done reading all the files
                if not self.READ : break # If we are pausing, we don't want to do any of the below
                self.updated.emit(100)
                self.READ = False
                self.reader.clearLastWord()
        except Exception as e:
            print("Something went wrong!\n" + str(e))

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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



