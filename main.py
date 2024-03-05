# hacky but here's why
#- https://github.com/dsdanielpark/Bard-API/issues/155
#- https://github.com/dsdanielpark/Bard-API/issues/99
# add funcs here: https://colab.research.google.com/drive/1zzzlTIh0kt2MdjLzvXRby1rWbHzmog8t?usp=sharing#scrollTo=gU9J5HUp7PfW
import requests
import sys
import threading, time
import queue
import signal
import pyttsx3
import browser_cookie3
import time
import keyboard
import speech_recognition as sr
import argparse
from bardapi import BardCookies
from cv2draw import CV2Draw
from quickdrawim import quickdoodle
from t2s import T2S

# for exiting the programs
def signal_handler(signum, frame):
    exit_event.set()

def user_input(query, ticket, exit_event, args):
    while True:
        if exit_event.is_set():
            print("kill reply")
            #time.sleep(1)
            sys.exit()
        time.sleep(0.1)
        if ticket.is_set():
            try:
                if args.mode == 'speech' :
                    # Python Program that helps translate Speech to Text
                    t = []
                    with mic as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        while ticket.is_set():
                            if exit_event.is_set():
                                print("kill reply")
                                #time.sleep(1)
                                sys.exit()
                            try:
                                # The Program listens to the user voice input.
                                print('start speech recognition')
                                a = r.listen(source)
                                t_ = r.recognize_google(a).lower()
                                print("press spacebar to continue speech recognition. Press 's' to send query.")
                                t.append(t_)
                                if keyboard.read_key() == 's':
                                    t = ''.join(x for x in t)
                                    print(t)
                                    if 'guess' in t.split():
                                        im_request.set()
                                    else:
                                        ticket.clear()
                                        print("using ticket for query")
                                        query.put(t)
                                        print("sent query")
                            except sr.UnknownValueError:
                                print("No User Voice detected OR unintelligible noises detected OR the recognized audio cannot be matched to text !!!")
                                pass
                elif args.mode == 'keyboard':
                    if exit_event.is_set():
                        print("kill reply")
                        #time.sleep(1)
                        sys.exit()
                    q = input()
                    if not q == '':
                        if 'guess' in q.split():
                            im_request.set()
                        else:
                            ticket.clear()
                            print("using ticket for query")
                            query.put(q)
                            print("sent query")
            # seems redundant but necessary bc of ctrl-c EOF error
            except EOFError:
                print("kill input")
                exit_event.set()
                #sys.exit()
                pass   
        pass   
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='keyboard', choices=['keyboard', 'sign', 'speech'])
    args = parser.parse_args()
    SESSION_HEADERS = {
    "Host": "gemini.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://gemini.google.com",
    "Referer": "https://gemini.google.com/app",
    }
    signal.signal(signal.SIGINT, signal_handler)
    domain = '.google.com'
    firefox_cookies = browser_cookie3.firefox(domain_name=domain)
    psid = '__Secure-1PSID'
    dts = '__Secure-1PSIDTS'
    dcc = '__Secure-1PSIDCC'
    nid = 'NID'
    psid_value = None
    dts_value = None
    dcc_value = None
    nid_value = None
    for cookie in firefox_cookies:
        print(cookie)
        if cookie.name == psid:
            psid_value = cookie.value
        elif cookie.name == dts:
            dts_value = cookie.value
        elif cookie.name == dcc:
            dcc_value = cookie.value
        elif cookie.name == nid:
            nid_value = cookie.value
    cookie_dict = {
        "__Secure-1PSID": psid_value,
        "__Secure-1PSIDTS": dts_value,
        "__Secure-1PSIDCC": dcc_value,
    }
    session = requests.Session()
    session.cookies.set("__Secure-1PSID", psid_value)
    session.cookies.set( "__Secure-1PSIDCC", dcc_value)
    session.cookies.set("__Secure-1PSIDTS", dts_value)
    session.cookies.set("NID",nid_value)
    session.headers = SESSION_HEADERS
    bard = BardCookies(session=session, cookie_dict=cookie_dict)
    r = sr.Recognizer()
    mic = sr.Microphone()
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    #signal.signal(signal.SIGINT, signal_handler)
    query = queue.Queue(maxsize=1)
    doodle = queue.Queue(maxsize=1)
    speech = queue.Queue()
    ticket = threading.Event()
    im_request = threading.Event()
    exit_event = threading.Event()
    exit_t2s_event = threading.Event()
    u = threading.Thread(target=user_input, args=(query, ticket, exit_event, args))
    u.start()
    # cv draw
    cv2draw = CV2Draw()
    c = threading.Thread(target=cv2draw.capture, args=(query, ticket, im_request, exit_event, args))
    c.start()
    d = threading.Thread(target=quickdoodle, args=(doodle, exit_event))
    d.start()
    t2s = T2S()
    print('you are in {0} mode'.format(args.mode))
    s = threading.Thread(target=t2s.t2s_thread, args=(speech, exit_t2s_event))
    s.start()
    ticket.set()
    #guess = False
    txt_guide = []
    txt_files = ['user_info.txt', 'doodle_list.txt', 'doodle_guess_instruction.txt', 'doodle_guess_terms.txt', 'doodle_guess_again_terms.txt', 'doodle_guess_again_instruction.txt', 'doodle_extension_terms.txt']
    speech.put(['ask away'])
    print('ask away!')
    for txt in txt_files:
        with open(txt, 'r') as file:
           txt_guide.append(file.read())
    doodle_inquiry = txt_guide[0] + txt_guide[1] + txt_guide[2]
    while True:
        time.sleep(0.1)
        # so exit event happens
        try:
            if not query.empty():
                reply = query.get()
                if type(reply) == str:
                    #if guess:
                    if any(x for x in txt_guide[4].split() if x in reply):
                        speech.put(["got it.. hmmm I'll try again"])
                        print("got it.. hmmm I'll try again")
                        reply = bard.get_answer(txt_guide[4])['content']
                        draw_doodles = (list(x for x in txt_guide[1].split() if x in reply))
                        print(draw_doodles)
                        if draw_doodles:
                            for dood in draw_doodles:
                                doodle.put(dood)
                    elif any(x for x in txt_guide[5].split() if x in reply):
                        speech.put(["let me tell you a story"])
                        print("let me tell you a story")
                        reply = bard.get_answer(txt_guide[4])['content']
                        speech.put(reply)
                        print(reply)
                    else:
                        speech.put(["got your text.. please wait one sec.."])
                        print("got your text.. please wait one sec..")
                        reply = bard.get_answer(reply)['content']
                else:
                    speech.put(["got your image.. please wait one sec.."])
                    print("got your image.. please wait one sec..")
                    reply = bard.ask_about_image(doodle_inquiry, reply)['content']
                    draw_doodles = (list(x for x in txt_guide[1].split() if x in reply))
                    if draw_doodles:
                        for item in draw_doodles:
                            try:
                                doodle.put(item, block=False)
                            except queue.Full:
                                pass
                speech.put(reply)
                print(reply)
                print("done")
                ticket.set()
                print("issuing new ticket")
                #guess = True
        except KeyboardInterrupt:
            pass
        if exit_event.is_set():
            speech.put(["let's recap"])
            print("let's recap")
            reply = bard.get_answer("summarize everything we talked about this session")['content']
            speech.put(reply) 
            print(reply)
            exit_t2s_event.set()
            sys.exit()
        pass