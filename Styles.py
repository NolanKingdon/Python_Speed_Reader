class Styles():

    def __init__(self, mode):
        self.MAIN_STYLES = """ """
        self.TOP_STYLES = """ """
        self.WORD_STYLES = """ """
        self.FLOAT_STYLES = """ """
        self.EXTRA_STYLES = """ """
        self.setStyles(mode)
        self.mode = mode

    def setStyles(self, mode):
        self.mode = mode
        print(self.mode)
        # There are very limited supporting styles here.

        # **********************DARK MODE ********************
        if self.mode == "dark":
        #0f0f0f --> Background on dark mode
        #212121 --> Read progress on dark mode
        #303030 --> Buttons on darkmode
        #e8e8e8 --> Text on darkmode

            # Main window styles
            self.MAIN_STYLES = """
                background-color: #0f0f0f;
            """

            # Topbar styles
            self.TOP_STYLES = """

                QPushButton
                {
                    color: #e8e8e8;
                    background-color: #303030;
                }

                QPushButton::disabled
                {
                    background-color: #4f4e4e;
                    color: #b5b5b5;
                }

                QPushButton:hover
                {
                    cursor: pointer;
                }

                QSlider::groove:horizontal
                {
                    border: 1px solid #999999;
                    height: 2px; /*the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                }
                
                QSlider::handle:horizontal
                {
                     background-color: #00c5d7;
                     height: 20px;
                     width: 10px;
                     margin: -20px 0;
                }
                
            """

            # Read Words Styles
            self.WORD_STYLES = """

            QLabel
            {
                background-color: transparent;
                color: #d8d8d8;
            }

            QLabel#red-letter
            {
                color: red;
            }

            QProgressBar
            {
                border: 1px solid black;
                background-color: #171717;
                text-align: right;
                color: transparent;
            }
            
            QProgressBar::chunk
            {
                background-color: #212121;
                width: 1px;
            }

            """

            self.FLOAT_STYLES = """

            QLabel#wpm
            {
                color: #d8d8d8;
            }

            QCheckBox
            {
                color: #d8d8d8;
            }

            """

            self.EXTRA_STYLES = """

            QLabel#summary-paragraph
            {
                background-color: #171717;
                border: 1px solid black;
                text-align: center;
                color: #d8d8d8;
            }

            QLabel#current-file
            {
                color: #d8d8d8
            }
            
            """

        # ***************** NORMAL MODE *********************
        elif self.mode == "normal":

            self.MAIN_STYLES = """
                background-color: #f0f0f0;
            """
            
            self.TOP_STYLES = """

                QSlider::handle:horizontal
                {
                     background-color: #cedbf0;
                }
            """

            self.WORD_STYLES = """

            QLabel
            {
                background-color: transparent;
                color: black;
            }

            QLabel#red-letter
            {
                color: red;
            }

            QProgressBar
            {
                background-color: #FFFFFF;
                border: 1px solid black;
                text-align: right;
                color: transparent;
            }
            QProgressBar::chunk
            {
                background-color: #cedbf0;
                width: 1px;
            }
            """

            self.FLOAT_STYLES = """


            """

            self.EXTRA_STYLES = """

            QLabel#summary-paragraph
            {
                background-color: #FFFFFF;
                border: 1px solid black;
                text-align: center;
            }
            
            
            """


    
    def getStyles(self):
        return {
            'main':self.MAIN_STYLES,
            'top':self.TOP_STYLES,
            'word':self.WORD_STYLES,
            'float':self.FLOAT_STYLES,
            'extra':self.EXTRA_STYLES
            }

            
