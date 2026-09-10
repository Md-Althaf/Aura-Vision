import cv2
import json
import math
import time
import random
import numpy as np
import pyautogui
import pygame

from hand_detector import HandDetector
from camera import Camera
from gestures import Gestures

with open("config.json") as f:
    cfg = json.load(f)

camera = Camera(device=cfg["camera_device"], resolution=cfg["resolution"])
pyautogui.FAILSAFE = False
Gesture = Gestures()
detector = HandDetector()

pygame.mixer.init()

screen_X, screen_Y = pyautogui.size()

cv2.namedWindow("MyCamera", cv2.WINDOW_NORMAL)
window_w = int(screen_X * 0.8)
window_h = int(window_w * (camera.height / camera.width))
cv2.resizeWindow("MyCamera", window_w, window_h)

def dis(p1, p2, h, w):
    x1 = int(p1.x * w)
    x2 = int(p2.x * w)
    y1 = int(p1.y * h)
    y2 = int(p2.y * h)
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

def glitch(frame):
    out = frame.copy()
    h, w = out.shape[:2]
    block = 40
    for _ in range(20):
        x = random.randint(0, max(0, w - block))
        y = random.randint(0, max(0, h - block))
        channel = random.randint(0, 2)
        shift = random.randint(-25, 25)
        out[y:y+block, x:x+block, channel] = np.roll(out[y:y+block, x:x+block, channel], shift, axis=1)
    return out

prevpoint = None
last_trigger = 0
COOLDOWN = cfg["gesture_delay_seconds"]
Clicked = False
CLICK_THRESHOLD = cfg["click_sensitivity"]
DIR_THRESHOLD = cfg["gesture_sensitivity"]
SMOOTHNESS = cfg["cursor_smoothness"]
FLIP = 1 if cfg["mirror_camera"] else 0

smooth_x, smooth_y = screen_X / 2, screen_Y / 2
party_mode_until = 0

try:
    while True:
        frame = camera.read(flip=FLIP)
        if frame is None:
            continue

        results = detector.findHands(frame)
        h, w, _ = frame.shape

        if results.multi_hand_landmarks:
            for hand, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                detector.draw(frame, hand)

                currentpos = hand.landmark[0]
                L_fingers, R_fingers = detector.fcounts(hand, handedness)
                movement = detector.direction(currentpos, prevpoint, w, h, DIR_THRESHOLD)

                if L_fingers == [0,1,0,0,0] or R_fingers == [0,1,0,0,0]:
                    index_tip = hand.landmark[8]
                    target_x = index_tip.x * screen_X
                    target_y = index_tip.y * screen_Y
                    smooth_x += (target_x - smooth_x) * (1 - SMOOTHNESS)
                    smooth_y += (target_y - smooth_y) * (1 - SMOOTHNESS)
                    cursor_x = max(0, min(screen_X - 1, int(smooth_x)))
                    cursor_y = max(0, min(screen_Y - 1, int(smooth_y)))
                    pyautogui.moveTo(cursor_x, cursor_y)

                    pinch = dis(hand.landmark[4], hand.landmark[8], h, w)
                    if pinch < CLICK_THRESHOLD and not Clicked:
                        pyautogui.click()
                        Clicked = True
                    elif pinch >= CLICK_THRESHOLD:
                        Clicked = False
                else:
                    guess = Gesture.GesturesDetect(L_fingers, R_fingers, movement)
                    if guess is not None and time.time() - last_trigger > COOLDOWN:
                        last_trigger = time.time()
                        if guess == "party_mode":
                            party_mode_until = time.time() + 3.0
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.load(cfg["party_song_path"])
                                pygame.mixer.music.play()
                        else:
                            pyautogui.press(guess)
                            print(guess)
                            cv2.putText(frame, guess, (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                prevpoint = currentpos
        else:
            prevpoint = None

        if time.time() < party_mode_until:
            frame = glitch(frame)
            cv2.putText(frame, "ROCKSTAR MODE", (30, h // 2), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0,255,255), 3)

        cv2.imshow("MyCamera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('x') or key == ord('q'):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()
