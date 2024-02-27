import pyautogui as pyau
import time
import sys
from tqdm import tqdm

if len(sys.argv) != 3:
    print("Usage: python3 markAsAi_Vecteezy.py <number of pages to mark as AI> <name of pc>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        pass
    if pc == "oldboi":
        selectAll = (1188, 321)
        AiGenerated = (1571, 779)
        selectSoftware = (1572, 825)
        midJourney = (1557, 898)
        submitFor = (1588, 1021)
        submit = (647, 714)
        accept = (890, 799)

    clicks = [selectAll, AiGenerated, selectSoftware, midJourney, submitFor, submit, accept]

    for _ in tqdm(range(nPages), desc="Processing Pages", unit="page"):
        for i in range(7):
            pyau.moveTo(clicks[i])
            pyau.click()
            time.sleep(1)
        
        time.sleep(2)
        pyau.press('f5')
        time.sleep(4)


pages = int(sys.argv[1])
pc = sys.argv[2]

deleteWholePage(pages, pc)
