import pyautogui as pyau
import keyboard
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 submitWirestock.py <number of times to repeat.")
    sys.exit(1)

paused = False

def toggle_pause():
    global paused
    paused = not paused

keyboard.add_hotkey('p', toggle_pause)

def submitFiles(times):
    global paused
    for i in range(times):
        if paused:
            print("Paused. Press 'p' to resume.")
            while paused:
                time.sleep(0.1)
        print(f"{i+1} times  submited")
        # Select all
        pyau.moveTo(3211, 381)
        pyau.click()
        time.sleep(1)
        # Select AI Generated
        pyau.moveTo(3457, 498)
        pyau.click()
        time.sleep(1)
        # platform drop down
        pyau.moveTo(3565, 573)
        pyau.click()
        time.sleep(1)
        # Midjourney
        pyau.moveTo(3550, 648)
        pyau.click()
        time.sleep(1)
        # Submit
        pyau.moveTo(3636, 1259)
        pyau.click()
        time.sleep(30)

submitFiles(int(sys.argv[1]))
