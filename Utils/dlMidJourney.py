import pyautogui as pyau
import keyboard
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python3 dlMidJourney.py <number of images to download> <pc name>")
    sys.exit(1)

paused = False

def toggle_pause():
    global paused
    paused = not paused

keyboard.add_hotkey('p', toggle_pause)

def download_images(nImages, pc):
    if pc == "medusa":
        dlButton = (1748,228)
        
    if pc == "oldboi":
        dlButton = (1197, 316)
       
    global paused
    for i in range(nImages):
        if paused:
            print("Paused. Press 'p' to resume.")
            while paused:
                time.sleep(0.1)
        print(f"{i+1} downloaded")
        pyau.moveTo(dlButton)
        pyau.click()
        time.sleep(1)
        keyboard.send("right")

download_images(int(sys.argv[1]), sys.argv[2])
