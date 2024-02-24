import pyautogui as pyau
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 pinocchio.py <number of pages to delete>")
    sys.exit(1)


def deleteWholePage(nPages):
    for _ in range(nPages):
        pyau.moveTo(1150, 1425)
        pyau.click()
        time.sleep(1)
        pyau.moveTo(1870, 1485)
        pyau.click()
        pyau.moveTo(944, 1479)
        time.sleep(1)
        pyau.click()
        time.sleep(15)


deleteWholePage(int(sys.argv[1]))

# while True:

#     # Get the current mouse position
#     x, y = pyau.position()

#     # Print the coordinates
#     print("Mouse X coordinate:", x)
#     print("Mouse Y coordinate:", y)
#     time.sleep(0.5)
