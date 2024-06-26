import pyautogui as pyau
import pyperclip
import time
import sys
import random
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python3 pinocchio.py <prompt list.txt>")
    sys.exit(1)


def isLunchBreak():
    current_time = datetime.now().time()
    randomMinute = int(random.uniform(1,10))
    lunch_start = datetime.strptime(f"12:0{randomMinute}", "%H:%M").time()
    randomMinute = int(random.uniform(1,10))
    lunch_end = datetime.strptime(f"13:0{randomMinute}", "%H:%M").time()
    return lunch_start <= current_time <= lunch_end

def isNapTime():
    current_time = datetime.now().time()
    randomMinute = int(random.uniform(1,10))
    awake_end = datetime.strptime(f"21:0{randomMinute}", "%H:%M").time()
    return current_time > awake_end

def sendPrompt(prompt, params):
    pyau.moveTo(600,600)

    pyau.click()
    time.sleep(random.uniform(3,10))
    pyperclip.copy("/imagine")
    pyau.hotkey('ctrl', 'v')
    time.sleep(random.uniform(3,10))

    pyau.press("enter")
    time.sleep(random.uniform(3,10))

    pyau.typewrite(prompt.strip())
    time.sleep(random.uniform(3,10))
    pyau.typewrite(" shot by hasselblad X1D, editorial photography  ")
    pyau.typewrite(params)

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
    print(f"Selected prompt: {prompt}")
    return prompt

promptsListPath = sys.argv[1] # Prompt list
promptList = getPromptList(promptsListPath)


time.sleep(10)


while True:        
    current_time = datetime.now().time()
    midday = datetime.strptime(f"12:00", "%H:%M").time()
    if current_time < midday:
        params = " --ar 2:1 --chaos 25 "
    else:
        params = " --ar 1:2 --chaos 25 "
 
    if not isNapTime() and not isLunchBreak():
        time.sleep(random.uniform(3 * random.uniform(40,60), 7 * random.uniform(40,60)))
        sendPrompt(getPrompt(), params)
        
    else:
        print("what")
        if isLunchBreak():
            print("Eating some bytes...")
            while isLunchBreak():
                print("Nom nom nom nom nom nom")
                time.sleep(60)
        elif isNapTime():
            print("Taking a nap....")
            while isNapTime():
                sys.exit(1)
        
    time.sleep(10)
