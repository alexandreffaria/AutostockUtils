import pyautogui as pyau
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python3 deleteAdobeStock.py <number of pages to delete> <name of the pc>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        selectAll = (1206, 1427)
        deleteIcon = (1877, 1490)
        confirmDelete = (980, 1482)
    if pc == "oldboi":
        selectAll = (1197, 316)
        deleteIcon = (1781, 328)
        confirmDelete = (914, 661)
    for _ in range(nPages):
        pyau.moveTo(selectAll)
        pyau.click()
        time.sleep(1)
        pyau.moveTo(deleteIcon)
        pyau.click()
        pyau.moveTo(confirmDelete)
        time.sleep(1)
        pyau.click()
        time.sleep(7)


deleteWholePage(int(sys.argv[1]), sys.argv[2])
