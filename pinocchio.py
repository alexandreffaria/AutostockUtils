import pyautogui as pyau
import time
import sys
import random
from datetime import datetime, timedelta

if len(sys.argv) != 2:
    print("Usage: python3 pinocchio.py <prompt list.txt>")
    sys.exit(1)

def isLunchBreak():
    current_time = datetime.now().strftime('%H:%M')
    lunch_start = datetime.strptime("12:00", "%H:%M").time()
    lunch_end = datetime.strptime("13:00", "%H:%M").time()
    print("time to eat? ", lunch_start <= current_time <= lunch_end)
    return lunch_start <= current_time <= lunch_end

def isNapTime():
    current_time = datetime.now().time()
    randomMinute = int(random.uniform(1,15))
    awake_start = datetime.strptime(f"08:{randomMinute:02}", "%H:%M").time()
    randomMinute = int(random.uniform(1,15))
    awake_end = datetime.strptime(f"21:{randomMinute:02}", "%H:%M").time()

    print(f"awake_start: {awake_start}, awake_end: {awake_end}, current_time: {current_time}")
    print("time for a nap? ", awake_start <= current_time <= awake_end)
    return awake_start <= current_time <= awake_end

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
    prompt = promptList[int(randomPrompt)]

    return prompt

promptsListPath = sys.argv[1] # Prompt list
promptList = getPromptList(promptsListPath)

time.sleep(5)


while True:        
    current_time = datetime.now().time()
    
    if not isNapTime() and not isLunchBreak():
        
        prompt = getPrompt()
        sendPrompt(prompt)

        sleep_duration = random.uniform(3 * 60, 7 * 60)

        time.sleep(sleep_duration)

        current_time = datetime.now().time()
        
    else:
        if isLunchBreak():
            print("Eating some bytes...")
        else:
            print("Taking a nap....")
        
        time.sleep(1000)
