import mediapipe as mp
import cv2

class HandDetector():
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        print(".......................Mediapipe--Initializing.......................")
    def findHands(self,frame):
       rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

       results = self.hands.process(rgb)
     
       return results
    def draw(self,frame,hand):
        self.mpDraw.draw_landmarks(frame,hand,self.mphands.HAND_CONNECTIONS)

    def handLorR(self,handedness):
        if handedness.classification[0].label == 'Right':
                return "Right"
        elif handedness.classification[0].label == 'Left':
                return "Left"
    
    def fcounts(self,hand,handedness):
        Tips_ids = [4,8,12,16,20]
        R_fingers = []
        L_fingers = []

        if self.handLorR(handedness) == 'Left':
            for tip in Tips_ids:
                 if tip == 4:
                    L_fingers.append(1 if hand.landmark[tip].x>hand.landmark[tip-2].x else 0)
                 else:
                    L_fingers.append(1 if hand.landmark[tip].y<hand.landmark[tip-2].y else 0)

        elif self.handLorR(handedness) == 'Right':
            for tip in Tips_ids:
                if tip == 4 :
                    R_fingers.append(1 if hand.landmark[tip].x<hand.landmark[tip-2].x else 0)
                else:
                    R_fingers.append(1 if hand.landmark[tip].y<hand.landmark[tip-2].y else 0)

        print(f''' Left {L_fingers} | Right {R_fingers}''')

        return L_fingers,R_fingers





         
    
