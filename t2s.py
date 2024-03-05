import pyttsx3
import sys
import time

class T2S:
    def __init__(self):
        self.t2s = pyttsx3.init()

    def t2s_thread(self, speech, exit_t2s_event):
        while True:
            if exit_t2s_event.is_set():
                print("kill t2s")
                #time.sleep(1)
                sys.exit()
            if not speech.empty():
                self.t2s.startLoop(False)
                self.t2s.say(speech.get())
                self.t2s.iterate()
                self.t2s.endLoop()
            time.sleep(1)
            