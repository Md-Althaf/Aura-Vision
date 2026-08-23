import pyautogui
class Controller():
    def __init__(self):
        self.Play = True
        self.ARcontroller = False
        self.Ccommands = ["playpause","nexttrack","prevtrack","volumemute","down","up"]

        print("_____________________Controller-Initialized_____________________")

    def send(self,command):
        print(command)
        if command  in self.Ccommands :
            if self.Play :
                pyautogui.press(command)
                print(command)
                self.Play = False
        else:
            
            self.Play = True
    def cursor(finger):
        x = finger.landmark.x
        y = finger.landmark.y
        pyautogui.moveTo(x,y)


