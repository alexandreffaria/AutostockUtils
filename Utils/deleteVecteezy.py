import pyautogui as pyau
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python3 script.py <number of pages to delete> <medusa or oldboi>")
    sys.exit(1)


def deleteWholePage(nPages, pc):
    if pc == "medusa":
        selectAll = (1210, 352)
        deleteIcon = (1794, 292)
        confirmDelete = (916, 616)
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
        pyau.click()
        time.sleep(1)
        time.sleep(8)


deleteWholePage(int(sys.argv[1]), sys.argv[2])
