import pyautogui as pyau
import keyboard
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python3 deleteLembrete.py <number of times to repeat.")
    sys.exit(1)

paused = False

def toggle_pause():
    global paused
    paused = not paused

keyboard.add_hotkey('p', toggle_pause)

def submitFiles(times):
    global paused
    for i in range(times):
        if paused:
            print("Paused. Press 'p' to resume.")
            while paused:
                time.sleep(0.1)
        print(f"{i+1} times  submited")
        # Select image
        pyau.moveTo(130, 410)
        pyau.click()
        time.sleep(1)
        # Corrigir e enviar
        pyau.moveTo(1699, 965)
        pyau.click()
        time.sleep(1)
        # Excluir
        pyau.moveTo(1869, 348)
        pyau.click()
        time.sleep(1)
        # Confirmar
        pyau.moveTo(953, 477)
        pyau.click()
        time.sleep(3)
        

submitFiles(int(sys.argv[1]))
