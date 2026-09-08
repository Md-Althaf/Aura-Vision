import cv2

def find_camera(max_index=5):
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            cap.release()
            return i
    return None

class Camera:
    def __init__(self,device = 0,width=680,height=480): 

        print("...........Camera--Initialized............")
        if device == "auto":
            found = find_camera()
            if found is None:
                raise Exception("No working camera found on this device")
            device = found

        self.device = device
        self.capture = cv2.VideoCapture(device)

        if not self.isOpened():
            raise Exception("unable to open camera")

        if resolution != "auto":
            width, height = resolution
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        actual_w = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.width = actual_w
        self.height = actual_h
        print(f"Camera Opened -> device {device}, {actual_w}x{actual_h}, ~{actual_fps:.0f} fps")

    def read(self, flip=1):
        success, frame = self.capture.read()
        if not success or frame is None:
            return None
        if flip:
            frame = cv2.flip(frame, 1)
        return frame
        
    def release(self):
        self.capture.release()
    def isOpened(self):
        return self.capture.isOpened()
    
    
