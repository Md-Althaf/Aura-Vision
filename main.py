import cv2
import mediapipe as mp
import math 
import pyautogui

from hand_detector import HandDetector
from camera import Camera
from gestures import Gestures

camera = Camera()

pyautogui.FAILSAFE = False
play = True

detector = HandDetector()

screen_X,screen_Y = pyautogui.size()
Clicked = False

def dis(p1,p2,h,w):
    x1 = int(p1.x*w)
    x2 = int(p2.x*w)
    y1 = int(p1.y*h)
    y2 = int(p2.y*h)
    dis = (x2-x1)**2 + (y2-y1)**2
    return int(math.sqrt(dis))

prevpoint = None
prevpointthumb = None
ddis = 0
while_run = True

while while_run:
    frame  = camera.read()

    results = detector.findHands(frame)
    h,w,_ = frame.shape
    
    if results.multi_hand_landmarks:
        for hand,handedness in zip(results.multi_hand_landmarks,results.multi_handedness):

            detector.draw(frame,hand)

            currentpos = hand.landmark[0]
            
            L_fingers , R_fingers = detector.fcounts(hand,handedness)
            movement = detector.direction(currentpos,prevpoint)

            if R_fingers == [0,1,1,0,0]:
                if play:
                    pyautogui.press("playpause")
                    play = False
            else:
                play = True
            print(Gestures.GesturesDetect(L_fingers,R_fingers,movement))

            prevpoint = currentpos
    cv2.imshow("MyCamera",frame)


    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

camera.release()
cv2.destroyAllWindows()



