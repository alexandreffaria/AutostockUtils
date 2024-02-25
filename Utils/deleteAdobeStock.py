import pyautogui as pyau
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 pinocchio.py <number of pages to delete>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        selectAll = (1165, 1355)
        deleteIcon = (1871, 1421)
        confirmDelete = (999, 1484)
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
        time.sleep(15)


deleteWholePage(int(sys.argv[1]), sys.argv[2])
