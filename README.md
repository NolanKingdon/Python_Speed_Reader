# Python Speed Reader

This is an application based on the idea that we would read much faster should
our eyes not have to move word to word.

This application will parse files and present them to the user one word at a time.

## Supported Filetypes

- .PDF
⋅⋅* This is currently being developed and is very hit-or-miss right now
- .DOCX
- .PPTX
- .TXT

I am planning on expanding into .HTML, and improving the .PDF in the future.

## Examples

![Speed Reader in Action](https://github.com/NolanKingdon/Python_Speed_Reader/blob/master/imgs/sample.PNG "Example of the Reader running")
![Speed Reader in Action](https://github.com/NolanKingdon/Python_Speed_Reader/blob/master/imgs/sample2.PNG "")

## Installing

To install this program use `git clone https://github.com/NolanKingdon/Python_Speed_Reader.git`

Then run `pip install -r requirements.txt`

## Running the reader

As this is a console based application, you will need to open your terminal/command line and navigate to the folder
the script is held in. then, open the file with python `python consoleUI.py` and follow the prompts

**Please note that this application will not work if run through IDLE.** This program makes use of the os.system(clear) command,
and is reliant on being openned in the terminal OR in the command prompt
