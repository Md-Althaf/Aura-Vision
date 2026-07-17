import cv2
import mediapipe as mp
import math 
import pyautogui

pyautogui.FAILSAFE = False
url = "https://192.168.43.13:8080"
url1 = "https://10.201.99.21:8080"
camera = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(False,1,1,0.5,0.5)
mpdraw = mp.solutions.drawing_utils

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
    ret, frame  = camera.read()
    frame = cv2.flip(frame,1)
    if not ret:
        break

    rgbframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(rgbframe)
    L_fingers = []
    R_fingers = []
    h,w,_ = frame.shape
    
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(frame,hand,mphands.HAND_CONNECTIONS)

            h,w,channels = frame.shape
            startpoint = hand.landmark[8]
            startpointthump = hand.landmark[4]
            if hand.landmark[4].x<hand.landmark[20].x :

                L_fingers.append(1 if hand.landmark[4].x<hand.landmark[2].x else 0)
                L_fingers.append(1 if hand.landmark[8].y<hand.landmark[6].y else 0)
                L_fingers.append(1 if hand.landmark[12].y<hand.landmark[10].y else 0)
                L_fingers.append(1 if hand.landmark[16].y<hand.landmark[14].y else 0)
                L_fingers.append(1 if hand.landmark[20].y<hand.landmark[18].y else 0)

            if hand.landmark[4].x>hand.landmark[20].x :

                R_fingers.append(1 if hand.landmark[4].x>hand.landmark[2].x else 0)
                R_fingers.append(1 if hand.landmark[8].y<hand.landmark[6].y else 0)
                R_fingers.append(1 if hand.landmark[12].y<hand.landmark[10].y else 0)
                R_fingers.append(1 if hand.landmark[16].y<hand.landmark[14].y else 0)
                R_fingers.append(1 if hand.landmark[20].y<hand.landmark[18].y else 0)

            
            


            
            print(f''' Left {L_fingers} | Right {R_fingers}''')
            if prevpoint is not None:
                ddis = dis(startpoint,prevpoint,h,w)
                print(ddis)
            
            

            if dis(hand.landmark[8],hand.landmark[4],768,1366)<30:
                if not Clicked:
                    pyautogui.click()
                    cv2.waitKey(10)
                    cv2.putText(frame, "CLICK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    Clicked = True
                else:
                    Clicked = False
            if ddis>10:
                cursor_x = int(hand.landmark[8].x*screen_X)
                cursor_y = int(hand.landmark[8].y*screen_Y)
            if ddis>10:
                pyautogui.moveTo(cursor_x,cursor_y,False)
            if dis(hand.landmark[4],hand.landmark[20],h,w)<30:
                pyautogui.press("playpause")
            elif dis(hand.landmark[12],hand.landmark[4],h,w)<30:
                print("breakdown")
                while_run = False
                break
            print(dis(hand.landmark[8],hand.landmark[4],h,w))
            if sum(L_fingers) == 2 :
                PREVDIS = dis(prevpointthumb,prevpoint,h,w)
                startdis = dis(startpointthump,startpoint,h,w)
                if PREVDIS<startdis:
                    for i in range(int(PREVDIS-startdis)):
                        pyautogui.press("volumeUp")
                        print("up")
                elif PREVDIS>startdis:
                    for i in range(int(PREVDIS-startdis)):
                        pyautogui.press("volumeDown")
                        print("down")

                    
            
            

            prevpoint = startpoint
            if prevpointthumb is not None:
                continue
            prevpointthumb = startpointthump
    cv2.imshow("MyCamera",frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

camera.release()
cv2.destroyAllWindows()



