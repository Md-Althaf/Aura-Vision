import mediapipe as mp
import cv2

class HandDetector():
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,frame):
       rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

       results = self.hands.process(rgb)
       return results
    def draw(self,frame,hand):
        self.mpDraw.draw_landmarks(frame,hand,self.mphands.HAND_CONNECTIONS)
    
    def fcounts(self,hand,L_fingers,R_fingers):

        if hand.landmark[4].x<hand.landmark[20].x :

                L_fingers.append(1 if hand.landmark[4].x<hand.landmark[2].x else 0)
                L_fingers.append(1 if hand.landmark[8].y<hand.landmark[6].y else 0)
                L_fingers.append(1 if hand.landmark[12].y<hand.landmark[10].y else 0)
                L_fingers.append(1 if hand.landmark[16].y<hand.landmark[14].y else 0)
                L_fingers.append(1 if hand.landmark[20].y<hand.landmark[18].y else 0)

        elif hand.landmark[4].x>hand.landmark[20].x :

                R_fingers.append(1 if hand.landmark[4].x>hand.landmark[2].x else 0)
                R_fingers.append(1 if hand.landmark[8].y<hand.landmark[6].y else 0)
                R_fingers.append(1 if hand.landmark[12].y<hand.landmark[10].y else 0)
                R_fingers.append(1 if hand.landmark[16].y<hand.landmark[14].y else 0)
                R_fingers.append(1 if hand.landmark[20].y<hand.landmark[18].y else 0)  

        print(f''' Left {L_fingers} | Right {R_fingers}''')

    def direction(self,currentpoint,prevpoint):
         if prevpoint is not None:
            
                dx = currentpoint.x - prevpoint.x
                dy = currentpoint.y - prevpoint.y
                dx *=640
                dy *=480
                
                print(f'''dx:{dx}|dy:{dy}''')
                Threshold = 50
                if dx>Threshold:
                    print("Left")
                elif dx<-Threshold:
                    print("Right")
                elif dy>Threshold:
                    print("Down")
                elif dy<-Threshold:
                    print("Up")

         
    
