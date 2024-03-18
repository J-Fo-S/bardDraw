# hacky but here's why
#- https://github.com/dsdanielpark/Bard-API/issues/155
#- https://github.com/dsdanielpark/Bard-API/issues/99
# add funcs here: https://colab.research.google.com/drive/1zzzlTIh0kt2MdjLzvXRby1rWbHzmog8t?usp=sharing#scrollTo=gU9J5HUp7PfW
import requests
import sys
import os
import threading, time
import queue
import signal
import pyttsx3
import browser_cookie3
import time
import keyboard
import speech_recognition as sr
import argparse
import csv
from collections import deque
from bardapi import BardCookies
from cv2draw import CV2Draw
from t2s import T2S


# for exiting the threads
def signal_handler(signum, frame):
    exit_event.set()

def reply_log(single_reply, self_refine, critic_refine):
    # setup to timestamp whatever scores to csv file
    with open('session.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["single reply", "self-refined reply", "critic-refined reply"])
        if self_refine:
            writer.writerow([single_reply.popleft(), self_refine.popleft(), "N/A"])
        elif critic_refine:
            writer.writerow([single_reply.popleft(), "N/A", critic_refine.popleft()])
        elif single_reply:
                writer.writerow([single_reply.popleft(), "N/A", "N/A"])
        print("_session saved to csv")
        sys.exit()

def user_input(query, ticket, exit_event, args):
    while True:
        # exit thread
        if exit_event.is_set():
            print("_kill reply")
            #time.sleep(1)
            sys.exit()
        time.sleep(0.1)
        if ticket.is_set():
            try:
                if args.user_mode == 'speech' :
                    t = []
                    with mic as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        while ticket.is_set():
                            #exit loop
                            if exit_event.is_set():
                                print("_kill reply")
                                sys.exit()
                            try:
                                # The Program listens to the user voice input.
                                print('_start speech recognition')
                                a = r.listen(source)
                                t_ = r.recognize_google(a).lower()
                                print("_press spacebar to continue speech recognition. Press 's' to send query.")
                                t.append(t_)
                                # send recorded speech
                                if keyboard.read_key() == 's':
                                    t = ''.join(x for x in t)
                                    print(t)
                                    if 'guess' in t.split():
                                        im_request.set()
                                    else:
                                        ticket.clear()
                                        print("_using ticket for query")
                                        query.put(t)
                                        print("_sent query")
                            except sr.UnknownValueError:
                                print("_No User Voice detected OR unintelligible noises detected OR the recognized audio cannot be matched to text !!!")
                                pass
                elif args.user_mode == 'keyboard':
                    q = input()
                    if not q == '':
                        if 'guess' in q.split():
                            im_request.set()
                        else:
                            ticket.clear()
                            print("_using ticket for query")
                            query.put(q)
                            print("_sent query")
            # seems redundant but necessary bc of ctrl-c EOF error
            except EOFError:
                print("_kill input")
                exit_event.set()
                pass   
        pass   
    
if __name__ == '__main__':
    #suppress errors/warnings
    #sys.stderr = open(os.devnull, "w")
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_mode', type=str, default='keyboard', choices=['keyboard', 'sign', 'speech'])
    parser.add_argument('--ref_mode', type=str, default='text_ref', choices=['text_ref', 'self_ref', 'critic_ref'])
    parser.add_argument('--mode_len', type=int, default=20, help='number of frames to evaluate gesture classification')
    parser.add_argument('--smooth', type=float, default=0.9, help='val between 0 and 1 to smooth drawing')
    args = parser.parse_args()
    # bard/gemini API stuff
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
    if args.ref_mode == 'critic_ref':
        bard_critic = BardCookies(session=session, cookie_dict=cookie_dict)
    # set up speech/mic input
    r = sr.Recognizer()
    mic = sr.Microphone()
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(r, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    # queue for bard queries
    query = queue.Queue(maxsize=1)
    # queue for generating doodles
    doodle = queue.Queue(maxsize=1)
    # queue for generating speech
    speech = queue.Queue()
    # deque for saving end results
    single_reply = deque()
    self_refine = deque()
    critic_refine = deque()
    # event for polling for queries
    ticket = threading.Event()
    # event for collecting cv2 image
    im_request = threading.Event()
    # event for exit threads
    exit_event = threading.Event()
    # staggered exit event so recap speech completes
    exit_t2s_event = threading.Event()
    user_in = threading.Thread(target=user_input, args=(query, ticket, exit_event, args))
    user_in.start()
    # cv draw
    cv2draw = CV2Draw()
    # threads for running concurrent programs
    cv_draw = threading.Thread(target=cv2draw.capture, args=(query, ticket, im_request, exit_event, args))
    cv_draw.start()
    draw_doodle = threading.Thread(target=cv2draw.quickdoodle, args=(doodle, exit_event))
    draw_doodle.start()
    t2s = T2S()
    print('_you are in {0} user_mode'.format(args.user_mode))
    computer_speech = threading.Thread(target=t2s.t2s_thread, args=(speech, exit_t2s_event))
    computer_speech.start()
    session_csv = threading.Thread(target=reply_log, args=(single_reply, self_refine, critic_refine))
    # start off polling
    ticket.set()
    # collect text guidence files
    txt_guide = []
    txt_files = ['user_info.txt', 'doodle_list.txt', 'doodle_guess_instruction.txt', 'doodle_guess_terms.txt',
                  'doodle_guess_again_terms.txt', 'doodle_guess_again_instruction.txt', 'doodle_extension_terms.txt', 
                  'doodle_extension_instruction.txt', 'doodle_recap_instruction.txt', 'doodle_refine_instruction.txt']
    speech.put(['ask away'])
    print('ask away!')
    for txt in txt_files:
        with open(txt, 'r') as file:
           txt_guide.append(file.read())
    # compose doodle inquiry from user info, doodle list and instruction
    doodle_inquiry = txt_guide[0] + txt_guide[1] + txt_guide[2]
    while True:
        time.sleep(0.1)
        try:
            if not query.empty():
                reply = query.get()
                if type(reply) == str:
                    # search for guess again terms
                    if any(x for x in txt_guide[4].split() if x in reply):
                        speech.put(["got it.. hmmm I'll try again"])
                        print("got it.. hmmm I'll try again")
                        reply = bard.get_answer(txt_guide[4])['content']
                        # TO-DO: fix bug of partial matchs (ant will be found in pants)
                        doodles = (list(x for x in txt_guide[1].split() if x in reply))
                        if doodles:
                            for dood in doodles:
                                print(f'_found {dood}')
                                doodle.put(dood)
                    # search for extension terms
                    elif any(x for x in txt_guide[6].split() if x in reply):
                        speech.put(["let me tell you"])
                        print("let me tell you")
                        reply = bard.get_answer(txt_guide[7])['content']
                    # free instruction - no matching terms
                    else:
                        speech.put(["got your text.. please wait one sec.."])
                        print("got your text.. please wait one sec..")
                        reply = bard.get_answer(reply)['content']
                # receive image from cv2draw
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
                print("reply: " + reply)
                # for .csv file
                single_reply.append(reply)
                if args.ref_mode == 'self_ref':
                    reply = bard.get_answer(txt_guide[9] + reply)['content']
                    print("reply self refined: " + reply)
                    self_refine.append(reply)
                elif args.ref_mode == 'critic_ref':
                    reply = bard_critic.get_answer(txt_guide[9] + reply)['content']
                    print("reply critic refined: " + reply)
                    critic_refine.append(reply)
                speech.put(reply)
                print("_done")
                ticket.set()
                print("_issuing new ticket")
                #guess = True
        except KeyboardInterrupt:
            pass
        if exit_event.is_set():
            speech.put(["let's recap"])
            print("let's recap")
            reply = bard.get_answer(txt_guide[8])['content']
            print("reply: " + reply)
            single_reply.append(reply)
            if args.ref_mode == 'self_ref':
                reply = bard.get_answer(txt_guide[9] + reply)['content']
                print("reply self refined: " + reply)
                self_refine.append(reply)
            elif args.ref_mode == 'critic_ref':
                reply = bard_critic.get_answer(txt_guide[9] + reply)['content']
                print("reply critic refined: " + reply)
                critic_refine.append(reply)
            session_csv.start()
            speech.put(reply) 
            exit_t2s_event.set()
            sys.exit()
        pass