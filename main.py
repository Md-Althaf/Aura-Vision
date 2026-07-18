import cv2
import mediapipe as mp
import math 
import pyautogui

from hand_detector import HandDetector
from camera import Camera

camera = Camera()

pyautogui.FAILSAFE = False

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


    rgbframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = detector.findHands(frame)
    L_fingers = []
    R_fingers = []
    h,w,_ = frame.shape
    
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            # detector.mpDraw.draw_landmarks(frame,hand,detector.mphands.HAND_CONNECTIONS)
            detector.draw(frame,hand)
            h,w,channels = frame.shape

            currentpos = hand.landmark[0]
            
            detector.fcounts(hand,L_fingers,R_fingers)
            detector.direction(currentpos,prevpoint)

            print(hand.landmark[0].z)
            prevpoint = currentpos
    cv2.imshow("MyCamera",frame)


    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

camera.release()
cv2.destroyAllWindows()



