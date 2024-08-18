import pyautogui as pyau
import time
import sys
import random
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file in the parent directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Get coordinates from environment variables
MOUSE_X1 = int(os.getenv('MOUSE_X1'))
MOUSE_Y1 = int(os.getenv('MOUSE_Y1'))
MOUSE_X2 = int(os.getenv('MOUSE_X2'))  
MOUSE_Y2 = int(os.getenv('MOUSE_Y2'))
MOUSE_X3 = int(os.getenv('MOUSE_X3'))  
MOUSE_Y3 = int(os.getenv('MOUSE_Y3'))

def is_lunch_break() -> bool:
    current_time = datetime.now().time()
    random_minute = int(random.uniform(1, 10))
    lunch_start = datetime.strptime(f"12:0{random_minute}", "%H:%M").time()
    random_minute = int(random.uniform(1, 10))
    lunch_end = datetime.strptime(f"13:0{random_minute}", "%H:%M").time()
    return lunch_start <= current_time <= lunch_end

def is_nap_time() -> bool:
    current_time = datetime.now().time()
    random_minute = int(random.uniform(1, 10))
    awake_end = datetime.strptime(f"21:0{random_minute}", "%H:%M").time()
    return current_time > awake_end

def send_prompt_to_coords(prompt: str, params: str, x: int, y: int) -> None:
    try:
        pyau.moveTo(x, y)
        pyau.click()
        time.sleep(random.uniform(3, 7))
        pyau.typewrite("/imagine")
        time.sleep(random.uniform(3, 7))
        pyau.press("enter")
        time.sleep(random.uniform(3, 7))
        pyau.typewrite(prompt.strip())
        time.sleep(random.uniform(3, 7))
        pyau.typewrite(params)
        pyau.press("enter")
        logging.info(f"Sent prompt: {prompt.strip()} with params: {params} to coordinates ({x}, {y})")
    except Exception as e:
        logging.error(f"Error sending prompt: {e}")

def get_prompt_list(prompts_list_path: str) -> list:
    try:
        with open(prompts_list_path, 'r') as f:
            prompt_list = [prompt.strip() for prompt in f]
        logging.info(f"Loaded {len(prompt_list)} prompts from {prompts_list_path}")
        return prompt_list
    except Exception as e:
        logging.error(f"Error loading prompt list: {e}")
        return []

def get_prompt(prompt_list: list) -> str:
    random_prompt = random.choice(prompt_list)
    logging.info(f"Selected prompt: {random_prompt}")
    return random_prompt

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python3 pinocchio.py <prompt list.txt>")
        sys.exit(1)

    prompts_list_path = sys.argv[1]
    prompt_list = get_prompt_list(prompts_list_path)

    if not prompt_list:
        logging.error("No prompts loaded. Exiting.")
        sys.exit(1)

    time.sleep(10)

    while True:
        current_time = datetime.now().time()
        midday = datetime.strptime("12:00", "%H:%M").time()
        afternoon_mid = datetime.strptime("17:00", "%H:%M").time()

        if current_time < midday:
            params = " --ar 2:1 --chaos 15 "
        elif midday <= current_time < afternoon_mid:
            params = " --ar 3:1 --chaos 15 "
        else:
            params = " --ar 1:2 --chaos 15 "

        if not is_nap_time() and not is_lunch_break():
            prompt = get_prompt(prompt_list)
            send_prompt_to_coords(prompt, params, MOUSE_X1, MOUSE_Y1)
            time.sleep(1)  # Short wait before sending to second window
            prompt = get_prompt(prompt_list)
            send_prompt_to_coords(prompt, params, MOUSE_X2, MOUSE_Y2)
            time.sleep(1)  # Short wait before sending to second window
            prompt = get_prompt(prompt_list)
            send_prompt_to_coords(prompt, params, MOUSE_X3, MOUSE_Y3)
            time.sleep(random.uniform(3 * random.uniform(40, 60), 7 * random.uniform(40, 60)))
        else:
            if is_lunch_break():
                logging.info("Eating some bytes... Nom nom nom")
                while is_lunch_break():
                    time.sleep(60)
            elif is_nap_time():
                logging.info("Taking a nap...")
                sys.exit(0)
        time.sleep(10)
