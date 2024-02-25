import pyautogui as pyau
import keyboard

# Lists to store coordinates and their indices
coordinates = []
indices = []


def get_mouse_position():
    # Get the current mouse position
    x, y = pyau.position()

    # Add the coordinates and their index to the lists
    coordinates.append((x, y))
    indices.append(len(coordinates))  # Add index

    # Print the index and coordinates
    print(f"{len(coordinates)}- Coordinates: ({x},{y})")


# Registering the hotkey
keyboard.add_hotkey("g", get_mouse_position)

# Keep the program running
keyboard.wait("esc")  # Press 'esc' to exit the program
