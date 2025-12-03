from decimal import _DecimalNew
import cv2
import numpy as np
import time
from mss import mss
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

keyboard = KeyboardController()
mouse = MouseController()
sct = mss()

# 1. Adjust to your Skyrim window coordinates
# Tip: Put Skyrim in WINDOWED 1280x720 mode and place it top-left of screen
monitor = {"top": 50, "left": 0, "width": 1280, "height": 720}

def press_key(key):
    keyboard.press(key)
    time.sleep(0.5)  # Held longer to ensure game registers it
    keyboard.release(key)

print("Starting Skyrim RL test in 5 seconds...")
print("Please ensure the Skyrim window is active and in the top-left corner.")
print("I will attempt to CLICK the window to focus it.")
time.sleep(5)

# Attempt to focus the window by clicking inside it
print("Clicking to focus...")
mouse.position = (100, 100)
mouse.click(Button.left, 1)
time.sleep(1)

for step in range(500):
    # ---- Capture frame ----
    frame = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # ---- Dumb AI action: press W every 10 frames ----
    if step % 10 == 0:
        print(f"[Step {step}] Pressing W")
        press_key('w')

    # ---- Show preview so you know it's working ----
    cv2.imshow("Skyrim Capture", frame)

    # ---- Exit if you press Q ----
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Done.")
cv2.destroyAllWindows()