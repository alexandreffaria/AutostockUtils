import pyautogui as pyau
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 pinocchio.py <number of pages to delete>")
    sys.exit(1)


def deleteWholePage(nPages):
    for _ in range(nPages):
        pyau.moveTo(1197, 316)
        pyau.click()
        time.sleep(1)
        pyau.moveTo(1781, 328)
        pyau.click()
        pyau.moveTo(914, 661)
        pyau.click()
        time.sleep(1)
        time.sleep(8)


deleteWholePage(int(sys.argv[1]))

# while True:

#     # Get the current mouse position
#     x, y = pyau.position()

#     # Print the coordinates
#     print("Mouse X coordinate:", x)
#     print("Mouse Y coordinate:", y)
#     time.sleep(3)
