import cv2
import mediapipe as mp
camera = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

while True:
    ret, frame  = camera.read()

    if not ret:
        break

    rgbframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(rgbframe)
    L_fingers = []
    R_fingers = []
    
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(frame,hand,mphands.HAND_CONNECTIONS)

            h,w,channels = frame.shape
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

            
            # print(f''' Left {L_fingers} | Right {R_fingers}''')
            print(hand)
            
            # cv2.putText(frame,str(fingers),(300,300),1,1,(0,0,255),1,1)
            


    cv2.imshow("MyCamera",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()



