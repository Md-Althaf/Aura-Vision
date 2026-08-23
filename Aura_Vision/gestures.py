import math
import Aura_Vision.controller as controller
class Gestures:
    def __init__(self):
        self.prevfingerL = None
        self.prevfingerR = None
        print("Gestures Initialized")
    def directions(self,hand,handtype,finger=0,handselect = "Right"):
        self.hand = hand
        current = hand.landmark[finger]
        if handtype == 'Right':
                if self.prevfingerR is None:
                    self.prevfingerR = current

                dx = current.x - self.prevfingerR.x
                dy = current.y - self.prevfingerR.y
                dx *= 640
                dy *= 480

                self.prevfingerR = current
                     
        elif handtype == 'Left' :
            if self.prevfingerL is None:
                    self.prevfingerL = current

            dx = current.x - self.prevfingerL.x
            dy = current.y - self.prevfingerL.y
            dx *= 640
            dy *= 480
            self.prevfingerL = current
                
        threshold= 80
        if handselect == handtype:
            if abs(dx) > abs(dy):
                if dx > threshold:
                        return "Right"
                elif dx < -threshold:
                        return "Left"
            else:
                if dy > threshold:
                    return "Down"
                elif dy < -threshold:
                    return "Up"

       
         
                
    def disBtwfingers(self,p1,p2,h,w):
            x1 = int(p1.x*w)
            x2 = int(p2.x*w)
            y1 = int(p1.y*h)
            y2 = int(p2.y*h)
            dis = (x2-x1)**2 + (y2-y1)**2
            return int(math.sqrt(dis))
         

                   
    def GesturesDetect(self,L_fingers,R_fingers,direction):
        if R_fingers == [0,1,1,0,0]:
            return "playpause"
        elif R_fingers == [0,1,0,0,0]:
            if direction == "Right":
                return "nexttrack"
            elif direction == "Left":
                 return "prevtrack"
        elif sum(R_fingers)<=2:
             if direction == "Up":
                  return "down"
             elif direction == "Down":
                  return "up"
        if L_fingers == [1,0,1,1,1]:
             return "volumemute"

        if L_fingers == [0,1,0,0,1]:
             return "AR Cursor"

             
        
        