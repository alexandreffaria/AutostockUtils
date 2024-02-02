import pyautogui as pyau
import time
import sys
import random
from datetime import datetime, timedelta

if len(sys.argv) != 2:
    print("Usage: python3 pinocchio.py <prompt list.txt>")
    sys.exit(1)

def getWorkHours():
    print("Getting working hours....")
    start_time = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))
    end_time = datetime.strptime("21:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))
    print(f"Working hours are: {start_time}-{end_time}")
    return start_time, end_time

def sendPrompt(prompt):
    pyau.moveTo(550,720)

    pyau.click()
    time.sleep(5)

    pyau.typewrite("/imaine")
    time.sleep(10)

    pyau.press("enter")
    time.sleep(5)

    pyau.typewrite(prompt.strip())
    time.sleep(5)
    pyau.typewrite(". Sony FE 24-70mm f/2.8 GM cinematic, shot by hasselblad X1D, editorial photogtaphy ")
    pyau.typewrite("--ar 16:9 --style raw")

    pyau.press("enter")



promptsList = sys.argv[1] # Prompt list

time.sleep(10)


start_time, end_time = getWorkHours()

while True:
        
    current_time = datetime.now().time()
    

    if start_time.time() <= current_time <= end_time.time():

        with open(promptsList, 'r') as f:

            for prompt in f:

                sendPrompt(prompt)

                sleep_duration = random.uniform(3 * 60, 7 * 60)

                time.sleep(sleep_duration)

                current_time = datetime.now().time()
                if not (start_time.time() <= current_time <= end_time.time()):
                    print("Time for a break c:")
                    break_duration = random.uniform(15,60)
                    time.sleep(break_duration * 60)

                    start_time = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))
                    end_time = datetime.strptime("21:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))

                    print(f"Back from break. New working hours: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
    else:
        print("in a break")
        time.sleep(10)

