import cv2

class Camera:
    def __init__(self,device = 0,width=680,height=480): 

        print("...........Camera--Initialized............")
        self.device =device
        self.width = width
        self.heigth = height

        self.capture = cv2.VideoCapture(device)

        if not self.isOpened():
            raise Exception("unable to open camera")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        print("Camera Opened")
    
    def read(self,flip=1):
        success , frame = self.capture.read()
        frame = cv2.flip(frame,flip)
        # if not success:
        #     raise Exception("Unable to read frame !!!")
        
        return frame
    def release(self):
        self.capture.release()
    def isOpened(self):
        return self.capture.isOpened()
    
    
