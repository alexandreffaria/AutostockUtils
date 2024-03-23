import pyautogui as pyau
import keyboard
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python3 dlMidJourney.py <number of pages to delete> <pc name>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        dlButton = (1747,1308)
        
    if pc == "oldboi":
        dlButton = (1197, 316)
       

    for _ in range(nPages):
        pyau.moveTo(dlButton)
        pyau.click()
        time.sleep(1)
        keyboard.send("right")
       


deleteWholePage(int(sys.argv[1]), sys.argv[2])
