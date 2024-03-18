### Draw and Tell with Gemini

This repo is an experimental prototype for Google ~~Bard~~[Gemini](https://gemini.google.com/), [Google Quickdraw](https://quickdraw.withgoogle.com/), OpenCV, speech recognition and Python. The purpose is for a person/child to draw a doodle with their fingers using OpenCV. Gemini tries to guess what the doodle is. Google Quickdraw is used to generate more doodles of what the drawing might be. The person/child can tell Gemini if the guess is correct or wrong via one of the following user_modes: keyboard input, microphone/speech input, or hand sign. If asked, Gemini will tell a story about the drawings. The end.

Sort of. Gemini happens to be a bit wonky at the moment, often explaining itself as an LLM, lecturing you about political correctness or creepily telling you about your current location. But all we wanted was Gemini to guess a simple drawing. The other purpose of this prototype is to try and guide Gemini to generate the most helpful and appropriate content for the user. There are three modes to achieve this: `--ref_mode text_ref` gives explicit instructions and context to Gemini. `--ref_mode self_ref` feeds Gemini back its own reply with instructions found in the `doodle_refine_instruction.txt` file. `--ref_mode critic_ref` creates a second instance of Gemini and instructs it to refine the first Gemini's response according to the same text file previously mentioned. Users may easily modify the text files but be sure to keep the same formatting. After you complete your session, you may compare the results of these "interventions" in the `sessions.csv` file.

#### Requirements

It is recommended to setup a [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and run `pip install -r requirements.txt` in the command line with the environment active. 

Also, you will need to install Firefox and have a wifi connection. You may need to open a Gemini session in Firefox first so the program can access the cookies. However, in my use this only needs to be done once - afterwards the cookies can be accessed even if the Firefox app is closed. 

This repo includes about 10 categories of Google Quickdraw data. If you want all 345 categories, download the bin files [here](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full;tab=objects?prefix=&forceOnObjectsSortingFiltering=false&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))) and update the `doodle_list.txt` file [accordingly](https://raw.githubusercontent.com/googlecreativelab/quickdraw-dataset/master/categories.txt) 

#### Running the code, drawing and interacting with Gemini

Here is a [quick demo](https://www.youtube.com/watch?v=06rEQQ3TD1Q) of what you should see when running the code, including some bugs and suboptimal performance of the free version of Gemini, opencv, my drawing skills, coding, etc.

`python main.py` will run the program with default user_mode of keyboard input. `--user_mode speech` and `--user_mode sign` are the other options. Once running, raise your right index finger to draw a thin line, and right index and middle finger to draw a thicker line. Right index, middle and ring finger will erase the drawing. In keyboard user_mode, type in the instructions (see the .txt files with "terms" in the title) you want Gemini to perform. Default .txt terms are "guess" to guess the drawing and "wrong" "try" "again" to ask Gemini to try again. Gemini is annoying and talks too much about itself, so the "instruction" .txt files are designed to try and task Gemini. Sometimes it sort of works. 

Speech user_mode is the same as keyboard user_mode, except you will need to press "s" to send the speech to Gemini. It should automatically record when clear speech is detected. Sign user_mode is more limited. Raise your left index finger to have Gemini guess about the drawing. Raise your left index and middle finger to have Gemini guess again. Raise your left index, middle and ring finger to have Gemini tell a story about the drawing (what Gemini guessed).

The other args `--smooth` and `--mode_len` control the drawing and number of frames to compute gesture recognition. Smooth must be between 0 and 1 while mode_len can be 1 through any number, but keep in mind we probably have 30 or so frames a second, so 30 might be a reasonable upper limit. 



 


