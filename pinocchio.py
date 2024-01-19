import pyautogui as pyau
import time
import sys
import random
from datetime import datetime, timedelta

if len(sys.argv) != 2:
    print("Usage: python script.py <file_path>")
    sys.exit(1)

start_time = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))
end_time = datetime.strptime("21:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))

file_path = sys.argv[1]

time.sleep(10)

while True:
        
    current_time = datetime.now().time()

    if start_time.time() <= current_time <= end_time.time():

        with open(file_path, 'r') as file:

            for line in file:

                pyau.moveTo(550,720)

                pyau.click()
                time.sleep(1)

                pyau.typewrite("/imagine")
                time.sleep(2)

                pyau.press("enter")
                time.sleep(1)

                pyau.typewrite(line.strip())
                time.sleep(1)
                pyau.typewrite(". Sony FE 24-70mm f/2.8 GM cinematic, shot by hasselblad X1D, editorial photogtaphy ")
                pyau.typewrite("--ar 16:9 --style raw")

                pyau.press("enter")

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
        print("Time to go to bed")

        break_duration = random.uniform(30,60)
        print(f'Break of : {break_duration}')
        time.sleep(break_duration * 60)
        start_time = datetime.strptime("08:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))
        end_time = datetime.strptime("21:00", "%H:%M") + timedelta(minutes=random.uniform(0,15))
        print(f"Back from break. New working hours: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")


