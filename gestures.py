class Gestures:
    def __init__(self):
        print("Gestures Initialized")
    def GesturesDetect(self,L_fingers,R_fingers,movement):

        if R_fingers == [0,1,1,0,0]:
            return "playpause"
        elif sum(R_fingers) == 5 and movement == "Right":
            return "nexttrack"
        elif sum(L_fingers) == 5 and movement == "Left":
            return "prevtrack"
        
            


