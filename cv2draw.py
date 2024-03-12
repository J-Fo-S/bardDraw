#https://techvidvan.com/tutorials/python-opencv-digital-drawing/
import cv2
import mediapipe as mp
import numpy as np
import sys
from collections import deque

class CV2Draw:
    
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(model_complexity=1,
                                        static_image_mode=False,
                                        max_num_hands=2,
                                        min_detection_confidence=0.5,
                                        min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
    
    def capture(self, query, ticket, im_request, exit_event, args):
        # For webcam input:
        canvas = np.ones((480, 640, 3), np.uint8) * 255
        last_point = None
        smooth = args.smooth
        mode_len = args.mode_len
        num_fingers_r_list =deque([], mode_len)
        num_fingers_l_list = deque([], mode_len)
        while self.cap.isOpened():
            if exit_event.is_set():
                print("_kill cv2")
                sys.exit()
            _, frame = self.cap.read()
            frame = cv2.resize(frame, (canvas.shape[0], canvas.shape[1]))
            x, y, c = frame.shape
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(framergb)
            gesture = ''
            answer = ''
            num_fingers_r = 0
            num_fingers_l = 0
            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)
                        landmarks.append([lmx, lmy])
                    self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)
                for hand in result.multi_handedness:
                    hand_lr = hand.classification[0].index
                    if hand_lr == 1:
                        if len(landmarks) > 0:
                            if landmarks[8][1] < landmarks[6][1]:
                                num_fingers_r += 1
                            if landmarks[12][1] < landmarks[10][1]:
                                num_fingers_r += 1
                            if landmarks[16][1] < landmarks[14][1]:
                                num_fingers_r += 1
                        num_fingers_r_list.append(num_fingers_r)
                        num_fingers_r_ave = max(set(num_fingers_r_list), key=num_fingers_r_list.count)
                        if num_fingers_r_ave == 1:
                            gesture = 'light line'
                        elif num_fingers_r_ave == 2:
                            gesture = 'heavy line'
                        elif num_fingers_r_ave == 3:
                            gesture = 'erase'
                    if hand_lr == 0 and args.mode == 'sign':
                        if len(landmarks) > 0:
                            if landmarks[8][1] < landmarks[6][1]:
                                num_fingers_l += 1
                            if landmarks[12][1] < landmarks[10][1]:
                                num_fingers_l += 1
                            if landmarks[16][1] < landmarks[14][1]:
                                num_fingers_l += 1
                        num_fingers_l_list.append(num_fingers_l)
                        num_fingers_l_ave = max(set(num_fingers_l_list), key=num_fingers_l_list.count)
                        if num_fingers_l_ave == 1:
                            answer = 'Guess the drawing'
                        elif num_fingers_l_ave == 2:
                            answer = 'Wrong, try again'
                        elif num_fingers_l_ave == 3:
                            answer = 'Right guess - tell a story'
                    #not necessary? # if canvas is not None:
                    if last_point is None:
                        last_point = landmarks[8]
                    current_point = (np.array(landmarks[8]) * (1-smooth) + np.array(last_point) * smooth).astype(int)
                    if gesture == 'light line':
                        if last_point is not None:
                            cv2.line(canvas, last_point, current_point, (0, 0, 0), 2)
                        last_point = current_point
                    elif gesture == 'heavy line':
                        if last_point is not None:
                            cv2.line(canvas, last_point, current_point, (0, 0, 0), 8)
                        last_point = current_point
                    elif gesture == 'erase':
                        cv2.rectangle(canvas, (0, 0), (canvas.shape[1], canvas.shape[0]), (255, 255, 255), -1)
                        last_point = None
                    else:
                        if last_point is not None:
                            last_point = landmarks[8]
            if (answer == 'Guess the drawing' or im_request.is_set()) and ticket.is_set():
                canvas_jpg = cv2.resize(canvas, (64, 64))
                _, canvas_jpg = cv2.imencode('.jpg', canvas_jpg)
                print("_using ticket for image")
                ticket.clear()
                print("_sending image")
                query.put(canvas_jpg.tobytes())
                if im_request.is_set():
                    im_request.clear()
            elif (answer == 'Right guess - tell a story' or answer == 'Wrong, try again') and ticket.is_set():
                print("_using ticket for query")
                ticket.clear()
                print("_sent query")
                query.put(answer)
            cv2.imshow("Board", canvas)
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(frame, answer, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA)
            cv2.imshow("Cam", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()