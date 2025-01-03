import pyautogui as pyau
import keyboard
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 freepikSubmit.py <number of times to repeat.")
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
        pyau.moveTo(299, 271)
        pyau.click()
        time.sleep(1)
        # Select AI Generated
        pyau.moveTo(1818, 995)
        pyau.click()
        time.sleep(1)
        # platform drop down
        pyau.moveTo(1124, 639)
        pyau.click()
        time.sleep(5)

submitFiles(int(sys.argv[1]))
