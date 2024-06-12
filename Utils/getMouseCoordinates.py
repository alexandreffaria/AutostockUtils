from pynput import mouse, keyboard

# Lists to store coordinates and their indices
coordinates = []
indices = []

def get_mouse_position():
    # Get the current mouse position
    with mouse.Controller() as mouse_controller:
        x, y = mouse_controller.position

    # Add the coordinates and their index to the lists
    coordinates.append((x, y))
    indices.append(len(coordinates))  # Add index

    # Print the index and coordinates
    print(f"{len(coordinates)}- Coordinates: ({x}, {y})")

def on_press(key):
    try:
        if key.char == 'g':
            get_mouse_position()
        elif key.char == 'q':  # Using 'q' to quit the program
            print("Exiting...")
            return False
    except AttributeError:
        pass

def main():
    # Start listening to the keyboard
    with keyboard.Listener(on_press=on_press) as listener:
        print("Press 'g' to get mouse position. Press 'q' to quit.")
        listener.join()

if __name__ == "__main__":
    main()
