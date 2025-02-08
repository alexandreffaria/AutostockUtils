import pyautogui as pyau
import keyboard
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 submitAdobe.py <number of times to repeat.")
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
        pyau.moveTo(1185, 396)
        pyau.click()
        time.sleep(1)
        # Select AI Generated
        pyau.moveTo(1678, 712)
        pyau.click()
        time.sleep(1)
        # Ficticious people
        pyau.moveTo(1662, 835)
        pyau.click()
        time.sleep(1)
        # send
        pyau.moveTo(1803, 201)
        pyau.click()
        time.sleep(8)
        # confirm
        pyau.moveTo(962, 905)
        pyau.click()
        time.sleep(10)
        # back
        pyau.moveTo(26, 63)
        pyau.click()
        time.sleep(5)

submitFiles(int(sys.argv[1]))
