# Proposed Image recognition system for better accessibility
## Pre-requisites

1. Clone this repo
2. Open command prompt or terminal
3. Navigate to the project folder `cd /path/to/capstone-ish/`
3. Run `pip install -r requirements.txt`

## Running the application

1. Open command prompt or terminal
2. Navigate to the project folder `cd /path/to/capstone-ish/`
3. Run `python .\UserInterface.py`

## Code
The application is split into 3 sections
1. UserInterface.py : 
Contains the user interface using tkinter. 
2. ImgToTxtApplication.py :
This is where the application will process the webpage.
It will perform:
- Web crawling to download all of the images in the web page
- Edit the webpage with the results from the ImageRecognizer.
- Generate a copy of modified webpage, text only of webpage, and downloaded images.

3. ImageRecognizer.py :  
This is where the images are translated to text using ImageAI and EasyOCR
