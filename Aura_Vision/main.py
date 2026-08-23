import cv2
import mediapipe as mp
import math 
import pyautogui
from Aura_Vision.controller import Controller

from Aura_Vision.hand_detector import HandDetector
from Aura_Vision.camera import Camera
from Aura_Vision.gestures import Gestures
url = "http://10.67.40.144:8080/video"
camera = Camera(0)

controller = Controller()
pyautogui.FAILSAFE = False
play = True
Gesture = Gestures()

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

prevhandL = None
prevhandR = None
ddis = 0
while_run = True
i = 0

while while_run:
    frame  = camera.read()

    results = detector.findHands(frame)
    h,w,_ = frame.shape
    
    if results.multi_hand_landmarks:
        for hand,handedness in zip(results.multi_hand_landmarks,results.multi_handedness):

            detector.draw(frame,hand)
            handtype = detector.handLorR(handedness)
            direction = Gesture.directions(hand,handtype,8)
            L_fingers , R_fingers = detector.fcounts(hand,handedness)
            handlora = detector.handLorR(handedness)
            command = Gesture.GesturesDetect(L_fingers,R_fingers,direction)
            if command == 'AR Cursor' and cursor:
                cursor = False
            else:
                cursor = True
                
                Controller.cursor(hand)
            controller.send(command)
        


    cv2.imshow("MyCamera",frame)


    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

camera.release()
cv2.destroyAllWindows()



