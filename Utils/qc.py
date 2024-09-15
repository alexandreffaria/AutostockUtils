import os
import sys
import shutil
import tkinter as tk
from PIL import Image, ImageTk
import logging
from dotenv import load_dotenv
import zipfile
import csv
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file in the parent directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Get icon path from environment variables
ICON_PATH = os.getenv('ICON_PATH', 'meulindo.ico')

def get_zip_files(folder_path: str) -> List[str]:
    """Get a list of .zip files in the folder."""
    return [item for item in os.listdir(folder_path) if item.lower().endswith('.zip')]

def unzip_file(file_path: str, extract_to: str) -> None:
    """Unzip a single zip file."""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def remove_file(file_path: str) -> None:
    """Remove a file."""
    os.remove(file_path)

def unzip_files(folder_path: str) -> None:
    """
    Unzip all .zip files in the specified folder.

    Args:
        folder_path (str): The path of the folder containing .zip files.
    """
    zip_files = get_zip_files(folder_path)

    for item in zip_files:
        file_path = os.path.join(folder_path, item)
        try:
            unzip_file(file_path, folder_path)
            logging.info(f"Unzipped {item}")
        except Exception as e:
            logging.error(f"Error unzipping file {item}: {e}")

    for item in zip_files:
        file_path = os.path.join(folder_path, item)
        try:
            remove_file(file_path)
            logging.info(f"Removed {item}")
        except Exception as e:
            logging.error(f"Error deleting file {item}: {e}")

def read_record_file(record_file_path: str) -> List[Tuple[str, str]]:
    """Read the record file and return a list of (file_name, action) tuples."""
    if not os.path.exists(record_file_path):
        return []
    try:
        with open(record_file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            records = [(row[0].strip(), row[1].strip()) for row in reader if len(row) == 2]
        return records
    except Exception as e:
        logging.error(f"Error reading record file: {e}")
        return []

def process_records(records: List[Tuple[str, str]], folder_path: str) -> None:
    """Process the records to delete or move images as previously recorded."""
    for file_name, action in records:
        file_path = os.path.join(folder_path, file_name)
        if action == 'delete':
            if os.path.exists(file_path):
                try:
                    remove_file(file_path)
                    logging.info(f"{file_name} deleted based on record file.")
                except Exception as e:
                    logging.error(f"Error deleting file {file_name}: {e}")
        elif action == 'letterbox':
            target_folder = os.path.join(folder_path, 'letterbox')
            os.makedirs(target_folder, exist_ok=True)
            target_path = os.path.join(target_folder, file_name)
            if os.path.exists(file_path):
                try:
                    shutil.move(file_path, target_path)
                    logging.info(f"{file_name} moved to 'letterbox' based on record file.")
                except Exception as e:
                    logging.error(f"Error moving file {file_name} to 'letterbox': {e}")

def get_image_files(folder_path: str, extensions: Tuple[str, ...]) -> List[str]:
    """Get a list of image files in the folder."""
    return [
        f for f in sorted(os.listdir(folder_path))
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(extensions)
    ]

def write_record_file(record_entries: Dict[str, str], record_file_path: str) -> None:
    """Write the record entries to the record file."""
    try:
        # Merge with existing records
        existing_records = dict(read_record_file(record_file_path))
        existing_records.update(record_entries)
        with open(record_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for file_name, action in existing_records.items():
                writer.writerow([file_name, action])
        logging.info("Record file updated.")
    except Exception as e:
        logging.error(f"Error writing record file: {e}")

def write_state_file(state_file_path: str, last_image: str) -> None:
    """Write the last viewed image to the state file."""
    try:
        with open(state_file_path, 'w') as f:
            f.write(last_image)
        logging.info(f"State file updated with last image: {last_image}")
    except Exception as e:
        logging.error(f"Error writing state file: {e}")

def read_state_file(state_file_path: str) -> str:
    """Read the last viewed image from the state file."""
    if not os.path.exists(state_file_path):
        return ''
    try:
        with open(state_file_path, 'r') as f:
            last_image = f.read().strip()
        logging.info(f"Last viewed image from state file: {last_image}")
        return last_image
    except Exception as e:
        logging.error(f"Error reading state file: {e}")
        return ''

class ImageViewer(tk.Tk):
    SHIFT_MASK = 0x0001  # Mask for the Shift key in event.state

    def __init__(self, folder_path: str, files: List[str], last_image: str = ''):
        super().__init__()

        self.folder_path = folder_path
        self.files = files
        self.current_index = 0
        self.actions_stack = []

        self.title("Image Viewer")
        self.geometry("800x600")
        self.configure(background="#2b2b2b")

        # Set window icon
        self.iconbitmap(ICON_PATH)

        self.viewer = tk.Label(self, bg="#2b2b2b")
        self.viewer.pack(expand=True, fill="both")

        # Bind the window close event
        self.protocol("WM_DELETE_WINDOW", self.close_viewer)

        # Load existing record entries
        record_file_path = os.path.join(self.folder_path, 'qc_record.txt')
        existing_records = read_record_file(record_file_path)
        self.record_entries = dict(existing_records)

        # Set current index based on last viewed image
        if last_image:
            try:
                self.current_index = self.files.index(last_image)
            except ValueError:
                logging.warning(f"Last viewed image '{last_image}' not found. Starting from the first image.")
                self.current_index = 0

        self.load_image()

        # Key bindings
        self.bind_keys()

    def bind_keys(self):
        """Bind keyboard and mouse events."""
        self.bind("<Right>", self.on_move_right)
        self.bind("<Left>", self.on_move_left)
        self.bind("<Key-h>", self.on_move_left)
        self.bind("<Key-l>", self.on_move_right)

        self.bind("<Key-x>", lambda event: self.mark_image_for_deletion())
        self.bind("<Delete>", lambda event: self.mark_image_for_deletion())
        self.bind("<Control_R>", lambda event: self.mark_image_for_deletion())
        self.bind("<Key-q>", lambda event: self.close_viewer())
        self.bind("<Key-w>", lambda event: self.move_image_to_folder("watermark"))
        self.bind("<Key-b>", lambda event: self.move_image_to_folder("letterbox"))
        self.bind("<Key-/>", lambda event: self.move_image_to_folder("letterbox"))
        self.bind("<BackSpace>", lambda event: self.undo_last_action())
        self.bind("<Return>", lambda event: self.copy_image_to_special())
        self.bind("<space>", lambda event: self.move_image_to_lulz())
        self.bind("<Key-t>", lambda event: self.move_image_to_tut())

        # Bind mouse wheel event
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<Button-4>", self.on_mouse_wheel)  # For Linux systems
        self.bind("<Button-5>", self.on_mouse_wheel)  # For Linux systems

    def shift_images(self, step: int) -> None:
        """Jump images by the given step."""
        new_index = self.current_index + step
        self.current_index = max(0, min(len(self.files) - 1, new_index))
        self.load_image()

    def on_mouse_wheel(self, event):
        shift_held = event.state & self.SHIFT_MASK
        if hasattr(event, 'delta'):
            if event.delta > 0:
                if shift_held:
                    self.shift_images(-10)
                else:
                    self.previous_image()
            else:
                if shift_held:
                    self.shift_images(10)
                else:
                    self.next_image()
        else:
            # For Linux systems
            if event.num == 4:
                if shift_held:
                    self.shift_images(-10)
                else:
                    self.previous_image()
            elif event.num == 5:
                if shift_held:
                    self.shift_images(10)
                else:
                    self.next_image()

    def close_viewer(self):
        last_image = self.files[self.current_index] if self.files else ''
        state_file_path = os.path.join(self.folder_path, 'qc_state.txt')
        write_state_file(state_file_path, last_image)

        self.destroy()
        record_file_path = os.path.join(self.folder_path, 'qc_record.txt')
        write_record_file(self.record_entries, record_file_path)

    def move_image_to_folder(self, target_folder: str) -> None:
        if not self.files:
            return

        file_name = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, file_name)
        target_folder_path = os.path.join(self.folder_path, target_folder)
        target_path = os.path.join(target_folder_path, file_name)

        try:
            os.makedirs(target_folder_path, exist_ok=True)
            shutil.move(source_path, target_path)
            logging.info(f"{file_name} moved to '{target_folder}' folder.")
            self.actions_stack.append(('move', target_folder, file_name))

            # Record the action if it's 'letterbox'
            if target_folder == 'letterbox':
                self.record_entries[file_name] = 'letterbox'

            del self.files[self.current_index]  # Remove the moved file from the list

            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1

            self.load_image()
        except Exception as e:
            logging.error(f"Error moving file {file_name} to {target_folder}: {e}")

    def on_move_right(self, event):
        if event.state & self.SHIFT_MASK:
            self.shift_images(10)
        else:
            self.next_image()

    def on_move_left(self, event):
        if event.state & self.SHIFT_MASK:
            self.shift_images(-10)
        else:
            self.previous_image()

    def next_image(self) -> None:
        if self.files:
            self.current_index = (self.current_index + 1) % len(self.files)
            self.load_image()

    def previous_image(self) -> None:
        if self.files:
            self.current_index = (self.current_index - 1) % len(self.files)
            self.load_image()

    def mark_image_for_deletion(self) -> None:
        if not self.files:
            return

        file_name = self.files[self.current_index]
        logging.info(f"{file_name} marked for deletion.")
        self.actions_stack.append(('delete', file_name))
        self.record_entries[file_name] = 'delete'  # Record the deletion
        del self.files[self.current_index]  # Remove the file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()

    def load_image(self) -> None:
        if not self.files:
            self.viewer.configure(image='')
            self.viewer.image = None
            self.title("Image Viewer")
            return

        file_name = self.files[self.current_index]
        file_path = os.path.join(self.folder_path, file_name)

        try:
            image = Image.open(file_path)

            # Get screen width and height
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Resize image to fit screen size
            image.thumbnail((screen_width, screen_height))

            photo = ImageTk.PhotoImage(image)
            self.viewer.configure(image=photo)
            self.viewer.image = photo

            self.title(f"{file_name} - {self.current_index + 1}/{len(self.files)}")
        except Exception as e:
            logging.error(f"Error loading image {file_name}: {e}")
            if len(self.files) > 1:
                self.next_image()  # Try loading the next image
            else:
                self.viewer.configure(image='')
                self.viewer.image = None
                self.title("Image Viewer")

    def undo_last_action(self) -> None:
        if not self.actions_stack:
            return

        action, *args = self.actions_stack.pop()
        file_name = args[-1]

        if action == 'move':
            target_folder = args[0]
            target_path = os.path.join(self.folder_path, target_folder, file_name)
            original_path = os.path.join(self.folder_path, file_name)
            try:
                shutil.move(target_path, original_path)
                logging.info(f"Undid move of {file_name} from '{target_folder}' back to original location.")
                self.files.insert(self.current_index, file_name)
                # Remove from record if necessary
                if self.record_entries.get(file_name) == 'letterbox':
                    del self.record_entries[file_name]
                self.load_image()
            except Exception as e:
                logging.error(f"Error undoing move of file {file_name}: {e}")
        elif action == 'delete':
            self.files.insert(self.current_index, file_name)
            logging.info(f"Undid deletion of {file_name}.")
            # Remove from record
            if self.record_entries.get(file_name) == 'delete':
                del self.record_entries[file_name]
            self.load_image()

    def copy_image_to_special(self) -> None:
        if not self.files:
            return

        file_name = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, file_name)
        special_folder_path = os.path.join(self.folder_path, '..', '..', 'Special')
        target_path = os.path.join(special_folder_path, file_name)

        try:
            os.makedirs(special_folder_path, exist_ok=True)
            shutil.copy2(source_path, target_path)
            logging.info(f"{file_name} copied to 'Special' folder.")
        except Exception as e:
            logging.error(f"Error copying file {file_name} to 'Special' folder: {e}")

    def move_image_to_lulz(self) -> None:
        self.move_image_to_external_folder('lulz')

    def move_image_to_tut(self) -> None:
        self.move_image_to_external_folder('tut')

    def move_image_to_external_folder(self, folder_name: str) -> None:
        if not self.files:
            return

        file_name = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, file_name)
        target_folder_path = os.path.join(self.folder_path, '..', '..', folder_name)
        target_path = os.path.join(target_folder_path, file_name)

        try:
            os.makedirs(target_folder_path, exist_ok=True)
            shutil.move(source_path, target_path)
            logging.info(f"{file_name} moved to '{folder_name}' folder.")
            self.actions_stack.append(('move', folder_name, file_name))
            del self.files[self.current_index]  # Remove the moved file from the list

            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1
            self.load_image()
        except Exception as e:
            logging.error(f"Error moving file {file_name} to '{folder_name}' folder: {e}")

def main() -> None:
    if len(sys.argv) != 2:
        logging.error("Usage: python3 qc.py /path/to/images")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        logging.error(f"The specified folder '{folder_path}' does not exist.")
        sys.exit(1)

    unzip_files(folder_path)

    record_file_path = os.path.join(folder_path, 'qc_record.txt')
    records = read_record_file(record_file_path)
    process_records(records, folder_path)

    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    files = get_image_files(folder_path, image_extensions)

    # Read last viewed image from state file
    state_file_path = os.path.join(folder_path, 'qc_state.txt')
    last_image = read_state_file(state_file_path)

    viewer = ImageViewer(folder_path, files, last_image)
    viewer.mainloop()

if __name__ == "__main__":
    main()
