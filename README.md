### Draw and Tell with ~~Bard~~Gemini

This repo is an experimental prototype for Google ~~Bard~~[Gemini](https://gemini.google.com/), [Google Quickdraw](https://quickdraw.withgoogle.com/), OpenCV, SpeechRecognition and Python. The purpose is for a person/child to draw a doodle with their fingers using OpenCV. Gemini tries to guess what the doodle is. Google Quickdraw is used to generate more doodles of what the drawing might be. The person/child can tell Gemini if the guess is correct or wrong via one of the following user_modes: keyboard input, microphone/speech input, or hand sign. If asked, Gemini will tell a story about the drawings. The end.

Sort of. I said this prototype was for Gemini to guess about a drawing. However, Gemini happens to be a bit wonky at the moment, often overexplaining itself, lecturing you about political correctness or creepily telling you about your current location. 

The other purpose of this prototype is to guide Gemini to generate the more helpful and appropriate content for the user. There are three modes to achieve this: `--ref_mode text_ref` submits explicit instructions and context to Gemini. These are found in the various `.txt` files and can be set once. This could be considered a "first order" method. `--ref_mode self_ref` feeds Gemini back its own reply with instructions found in the `doodle_refine_instruction.txt` file. This could be considered a "second order" method as Gemini is tasked with a second reply to refine its first reply. `--ref_mode critic_ref` takes this further and creates a second instance of Gemini with the instructions to refine the first Gemini's reply. Users may easily modify the text files but be sure to keep the same formatting. After you complete your session, you may compare the results of these "interventions" in the `sessions.csv` file.

### Example Comparing "first order" Gemini Reply with "Second Order" Critic Reply
Below, the critic Gemini is instructed to simply the first Gemini reply so a 4-year-old can understand, and to not talk about itself.

| First Order | Second Order |
| ----------- | ------------ |
|In this session, we had a conversation about what you might be drawing. I guessed that you were drawing a bird based on the limited information I have about your age and the potential clues in the image you might be creating.  We also discussed the challenges of accurately guessing a drawing without seeing it. 
|We talked about your drawing! It's hard to know for sure what it is without seeing it all, but maybe it's a bird?|


#### Requirements

It is recommended to setup a [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and run `pip install -r requirements.txt` in the command line with the environment active. 

Also, you will need to install Firefox and have a wifi connection. You may need to open a Gemini session in Firefox first so the program can access the cookies. However, in my use this only needs to be done once - afterwards the cookies can be accessed even if the Firefox app is closed. 

This repo includes about 10 categories of Google Quickdraw data. If you want all 345 categories, download the bin files [here](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full;tab=objects?prefix=&forceOnObjectsSortingFiltering=false&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))) and update the `doodle_list.txt` file [accordingly](https://raw.githubusercontent.com/googlecreativelab/quickdraw-dataset/master/categories.txt) 

#### Running the code, drawing and interacting with Gemini

Here is a [quick demo](https://youtu.be/vYItSylYNyE) of what you should see when running the code, including some bugs and suboptimal performance of the free version of Gemini, opencv, my drawing skills, coding, etc.

`python main.py` will run the program with default `--user_mode` of keyboard input and default `--ref_mode` of text_ref.

In `--user_mode keyboard` (default), type and enter in the instructions you want Gemini to perform. Recall that one purpose of this experiment is to guide Gemini's response, so the various `.txt` files contain key words and instructions that the key words trigger. Try modifying these. Default keywords are `guess` to guess the drawing and `wrong` `try` `again` to ask Gemini to try again.  

`--user_mode speech` functions similarly, except you simply speak instead of typing. When ready, press `s` to send the speech to Gemini. It should automatically record when clear speech is detected. `--user_mode sign` is more limited. Raise your left index finger to have Gemini guess about the drawing. Raise your left index and middle finger to have Gemini guess again. Raise your left index, middle and ring finger to have Gemini tell a story about the drawing (what Gemini guessed).

The `--ref_mode` options have been discussed in the introduction. The other args `--smooth` and `--mode_len` control the drawing and number of frames to compute gesture recognition. Smooth must be between 0 and 1 while mode_len can be 1 through any number, but keep in mind we probably have 30 or so frames a second, so 30 might be a reasonable upper limit. 

 To draw, you must press `up arrow` to enter draw mode. `Down arrow` will exit draw mode. Draw options are as follows:
1. raise your right index finger to draw a thin line 
2. raise your right index and middle finger to draw a thicker line 
3. raise your right index, middle and ring finger will erase the drawing. 



 


