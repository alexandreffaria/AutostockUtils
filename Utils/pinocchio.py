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
    lunch_end = datetime.strptime(f"12:2{randomMinute}", "%H:%M").time()
    return lunch_start <= current_time <= lunch_end

def isNapTime():
    current_time = datetime.now().time()
    randomMinute = int(random.uniform(1,10))
    awake_end = datetime.strptime(f"21:0{randomMinute}", "%H:%M").time()
    return current_time > awake_end

def sendPrompt(prompt, params):
    pyau.moveTo(1512,192)
    pyau.click()

    pyau.moveTo(775,984)
    pyau.click()

    time.sleep(random.uniform(3,10))
    pyperclip.copy("/imagine")
    pyau.hotkey('ctrl', 'v')
    time.sleep(random.uniform(3,10))

    pyau.press("enter")
    time.sleep(random.uniform(3,10))

    pyau.typewrite(prompt.strip())
    time.sleep(random.uniform(3,10))
    pyau.typewrite(" realistic, editorial ")
    pyau.typewrite(params)

    pyau.press("enter")

    pyau.moveTo(1512,192)
    pyau.click()

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
        params = " --ar 2:1 --chaos 5 "
    else:
        params = " --ar 2:1 --chaos 5 "
 
    if not isLunchBreak():
        time.sleep(random.uniform(1 * random.uniform(8,20), 3 * random.uniform(8,20)))
        sendPrompt(getPrompt(), params)
        
    else:
        print("what")
        if isLunchBreak():
            print("Eating some bytes...")
            while isLunchBreak():
                print("Nom nom nom nom nom nom")
                time.sleep(60)

                sys.exit(1)
        
    time.sleep(10)
