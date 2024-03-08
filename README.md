### Draw and Tell with Gemini

This repo is a dodgy experimental prototype for Google ~~Bard~~[Gemini](https://gemini.google.com/), [Google Quickdraw](https://quickdraw.withgoogle.com/), OpenCV, speech recognition and Python. The idea is that a person/child draws a doodle with their fingers using OpenCV. Gemini tries to guess what the doodle is. Google Quickdraw is used to generate more doodles of what the drawing might be. The person/child can tell Gemini if the guess is correct or wrong via one of the following modes: keyboard input, microphone/speech input, or hand sign. If asked, Gemini will tell a story about the drawings. The end.

Sort of. The other purpose of this prototype is to try and guide Gemini to generate the most helpful and appropriate content for the user. A primitive attempt at this is to include text files that give explicit instructions and context to Gemini. Users may easily modify these but be sure to keep the same formatting.

#### Requirements

It is recommended to setup a [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and run `pip install -r requirements.txt` in the command line with the environment active. 

Also, you will need to install Firefox and have a wifi connection. You may need to open a Gemini session in Firefox first so the program can access the cookies. However, in my use this only needs to be done once - afterwards the cookies can be accessed even if the Firefox app is closed. 

This repo includes about 10 categories of Google Quickdraw data. If you want all 345 categories, download the bin files [here](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full;tab=objects?prefix=&forceOnObjectsSortingFiltering=false&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))) and update the `doodle_list.txt` file [accordingly](https://raw.githubusercontent.com/googlecreativelab/quickdraw-dataset/master/categories.txt) 

#### Running the code, drawing and interacting with Gemini

`python main.py` will run the program with default mode of keyboard input. `--mode speech` and `--mode sign` are the other options. Once running, raise your right index finger to draw a thin line, and right index and middle finger to draw a thicker line. Right index, middle and ring finger will erase the drawing. In keyboard mode, type in the instructions (see the .txt files with "terms" in the title) you want Gemini to perform. Default .txt terms are "guess" to guess the drawing and "wrong" "try" "again" to ask Gemini to try again. Gemini is annoying and talks too much about itself, so the "instruction" .txt files are designed to try and task Gemini. Sometimes it sort of works. 

Speech mode is the same as keyboard mode, except you will need to press "s" to send the speech to Gemini. It should automatically record when clear speech is detected. Sign mode is more limited. Raise your left index finger to have Gemini guess about the drawing. Raise your left index and middle finger to have Gemini guess again. Raise your left index, middle and ring finger to have Gemini tell a story about the drawing (what Gemini guessed).

The other args `--smooth` and `--mode_len` control the drawing and number of frames to compute gesture recognition. Smooth must be between 0 and 1 while mode_len can be 1 through any number, but keep in mind we probably have 30 or so frames a second, so 30 might be a reasonable upper limit. 



 


