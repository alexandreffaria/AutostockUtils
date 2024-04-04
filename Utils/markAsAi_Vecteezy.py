import pyautogui as pyau
import time
import sys
import keyboard
from tqdm import tqdm

if len(sys.argv) != 3:
    print("Usage: python3 markAsAi_Vecteezy.py <number of pages to mark as AI> <name of pc>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        selectAll = (1233, 296)
        AiGenerated = (1593, 745)
        selectSoftware = (1592, 791)
        midJourney = (1563, 875)
        submitFor = (1583, 985)
        submit = (656, 672)
        accept = (909, 763)
    elif pc == "oldboi":
        selectAll = (1188, 321)
        AiGenerated = (1571, 779)
        selectSoftware = (1572, 825)
        midJourney = (1557, 898)
        submitFor = (1588, 1021)
        submit = (647, 714)
        accept = (890, 799)
    else:
        print("Invalid PC name.")
        sys.exit(1)

    clicks = [selectAll, AiGenerated, selectSoftware, midJourney, submitFor, submit, accept]

    for _ in tqdm(range(nPages), desc="Processing Pages", unit="page"):
        for i in range(7):
            pyau.moveTo(clicks[i])
            pyau.click()
            time.sleep(1)
        
        time.sleep(2)
        pyau.press('f5')
        time.sleep(4)

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
