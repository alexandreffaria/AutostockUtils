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

def isLunchBreak():
    current_time = datetime.now().time()
    lunch_start = datetime.strptime("12:00", "%H:%M").time()
    lunch_end = datetime.strptime("13:00", "%H:%M").time()

    return lunch_start <= current_time <= lunch_end

def sendPrompt(prompt):
    pyau.moveTo(550,720)

    pyau.click()
    time.sleep(5)

    pyau.typewrite("/imagine")
    time.sleep(10)

    pyau.press("enter")
    time.sleep(5)

    pyau.typewrite(prompt.strip())
    time.sleep(5)
    pyau.typewrite(". Sony FE 24-70mm f/2.8 GM cinematic, shot by hasselblad X1D, editorial photogtaphy ")
    pyau.typewrite("--ar 16:9 --style raw")

    pyau.press("enter")


def getPromptList(promptsListPath):
    promptList = []
    with open(promptsListPath, 'r') as f:
        for prompt in f:
            promptList.append(prompt)
    return promptList

def getPrompt():
    global promptList
    randomPrompt = random.uniform(0, len(promptList) - 1 )

    if currentPromptIndex >= len(promptList):
        currentPromptIndex = 0
    
    prompt = promptList[randomPrompt]

    return prompt

promptsListPath = sys.argv[1] # Prompt list
promptList = getPromptList(promptsListPath)
currentPromptIndex = 0

time.sleep(10)

start_time, end_time = getWorkHours()

while True:        
    current_time = datetime.now().time()
    
    if start_time.time() <= current_time <= end_time.time() and not isLunchBreak():
        
        prompt = getPrompt()
        sendPrompt(prompt)

        sleep_duration = random.uniform(3 * 60, 7 * 60)

        time.sleep(sleep_duration)

        current_time = datetime.now().time()
        
    else:
        if isLunchBreak():
            print("in a lunch break")
        else:
            print("in a bed")
        
        time.sleep(100)
