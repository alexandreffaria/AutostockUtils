import pyautogui as pyau
import time
import sys
import keyboard
from tqdm import tqdm

if len(sys.argv) != 3:
    print("Usage: python3 freepikSubmit.py <number of pages> <name of pc>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        selectAll = (292,298)
        submit = (1867,250)
    elif pc == "oldboi":
        selectAll = (292,298)
        submit = (1867,250)
        
    else:
        print("Invalid PC name.")
        sys.exit(1)

    clicks = [selectAll, submit]

    for _ in tqdm(range(nPages), desc="Processing Pages", unit="page"):
        for i in range(len(clicks)):
            pyau.moveTo(clicks[i])
            pyau.click()
            time.sleep(1)
        
        time.sleep(5)
        closeMessage = (1883,177)
        pyau.moveTo(closeMessage)
        pyau.click()
        

        if keyboard.is_pressed('esc'):
            print("Exiting...")
            sys.exit(0)
        elif keyboard.is_pressed('p'):
            print("Paused. Press 'p' to continue or 'esc' to kill.")
            while True:
                if keyboard.is_pressed('p'):
                    print("Resuming...")
                    break
                elif keyboard.is_pressed('esc'):
                    print("Exiting...")
                    sys.exit(0)


pages = int(sys.argv[1])
pc = sys.argv[2]

deleteWholePage(pages, pc)
