import pyautogui as pyau
import pyperclip
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
MOUSE_X = int(os.getenv('MOUSE_X', 623))
MOUSE_Y = int(os.getenv('MOUSE_Y', 723))

def is_lunch_break() -> bool:
    """
    Check if the current time is within the lunch break period.

    Returns:
        bool: True if it is lunch break, False otherwise.
    """
    current_time = datetime.now().time()
    random_minute = int(random.uniform(1, 10))
    lunch_start = datetime.strptime(f"12:0{random_minute}", "%H:%M").time()
    random_minute = int(random.uniform(1, 10))
    lunch_end = datetime.strptime(f"13:0{random_minute}", "%H:%M").time()
    return lunch_start <= current_time <= lunch_end

def is_nap_time() -> bool:
    """
    Check if the current time is within the nap time period.

    Returns:
        bool: True if it is nap time, False otherwise.
    """
    current_time = datetime.now().time()
    random_minute = int(random.uniform(1, 10))
    awake_end = datetime.strptime(f"21:0{random_minute}", "%H:%M").time()
    return current_time > awake_end

def send_prompt(prompt: str, params: str) -> None:
    """
    Send a prompt using pyautogui and pyperclip.

    Args:
        prompt (str): The prompt to send.
        params (str): Additional parameters for the prompt.
    """
    try:
        pyau.moveTo(MOUSE_X, MOUSE_Y)
        pyau.click()
        time.sleep(random.uniform(3, 10))
        pyperclip.copy("/imagine")
        pyau.hotkey('ctrl', 'v')
        time.sleep(random.uniform(3, 10))
        pyau.press("enter")
        time.sleep(random.uniform(3, 10))
        pyau.typewrite(prompt.strip())
        time.sleep(random.uniform(3, 10))
        pyau.typewrite(params)
        pyau.press("enter")
        logging.info(f"Sent prompt: {prompt.strip()} with params: {params}")
    except Exception as e:
        logging.error(f"Error sending prompt: {e}")

def get_prompt_list(prompts_list_path: str) -> list:
    """
    Get the list of prompts from a file.

    Args:
        prompts_list_path (str): The path to the file containing the prompts.

    Returns:
        list: A list of prompts.
    """
    try:
        with open(prompts_list_path, 'r') as f:
            prompt_list = [prompt.strip() for prompt in f]
        logging.info(f"Loaded {len(prompt_list)} prompts from {prompts_list_path}")
        return prompt_list
    except Exception as e:
        logging.error(f"Error loading prompt list: {e}")
        return []

def get_prompt(prompt_list: list) -> str:
    """
    Get a random prompt from the list.

    Args:
        prompt_list (list): The list of prompts.

    Returns:
        str: A random prompt.
    """
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
            send_prompt(get_prompt(prompt_list), params)
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
