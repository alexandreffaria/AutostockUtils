import os
import sys
import shutil
import tkinter as tk
from PIL import Image, ImageTk
import logging
from dotenv import load_dotenv
import zipfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file in the parent directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Get icon path from environment variables
ICON_PATH = os.getenv('ICON_PATH', 'meulindo.ico')

def unzip_files(folder_path: str) -> None:
    """
    Unzip all .zip files in the specified folder.

    Args:
        folder_path (str): The path of the folder containing .zip files.
    """
    zip_files = [
        item for item in os.listdir(folder_path) if item.lower().endswith('.zip')
    ]

    for item in zip_files:
        file_path = os.path.join(folder_path, item)
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            logging.info(f"Unzipped {item}")
        except Exception as e:
            logging.error(f"Error unzipping file {item}: {e}")

    for item in zip_files:
        file_path = os.path.join(folder_path, item)
        try:
            os.remove(file_path)
            logging.info(f"Removed {item}")
        except Exception as e:
            logging.error(f"Error deleting file {item}: {e}")

class ImageViewer(tk.Tk):
    def __init__(self, folder_path: str, files: list):
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

        self.load_image()

        self.bind("<Right>", lambda event: self.next_image())
        self.bind("<Left>", lambda event: self.previous_image())
        self.bind("<Key-x>", lambda event: self.mark_image_for_deletion())
        self.bind("<Control_R>", lambda event: self.mark_image_for_deletion())
        self.bind("<Key-q>", lambda event: self.close_viewer())
        self.bind("<Key-w>", lambda event: self.move_image_to_folder("watermark"))
        self.bind("<Key-b>", lambda event: self.move_image_to_folder("letterbox"))
        self.bind("<Key-/>", lambda event: self.move_image_to_folder("letterbox"))
        self.bind("<Key-h>", lambda event: self.previous_image())  # Binding 'h' to move left
        self.bind("<Key-l>", lambda event: self.next_image())
        self.bind("<BackSpace>", lambda event: self.undo_last_action())
        self.bind("<Return>", lambda event: self.copy_image_to_special())
        self.bind("<space>", lambda event: self.move_image_to_lulz())
        self.bind("<Key-t>", lambda event: self.move_image_to_tut())

        # Bind mouse wheel event
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<Button-4>", self.on_mouse_wheel)  # For Linux systems
        self.bind("<Button-5>", self.on_mouse_wheel)  # For Linux systems

        self.bind("<Shift-Left>", lambda event: self.shift_images(-10))
        self.bind("<Shift-Right>", lambda event: self.shift_images(10))


    def shift_images(self, step: int) -> None:
        """Jump images by the given step."""
        new_index = self.current_index + step
        self.current_index = max(0, min(len(self.files) - 1, new_index))
        self.load_image()

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.previous_image()
        else:
            self.next_image()

    def close_viewer(self):
        self.destroy()
        self.delete_marked_images()

    def move_image_to_folder(self, target_folder: str) -> None:
        if not self.files:
            return

        try:
            file_name = self.files[self.current_index]
            source_path = os.path.join(self.folder_path, file_name)
            target_folder_path = os.path.join(self.folder_path, target_folder)

            os.makedirs(target_folder_path, exist_ok=True)

            target_path = os.path.join(target_folder_path, file_name)
            shutil.move(source_path, target_path)

            logging.info(f"{file_name} moved to '{target_folder}' folder.")
            self.actions_stack.append(('move', target_folder, file_name))
            del self.files[self.current_index]  # Remove the moved file from the list

            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1

            self.load_image()
        except Exception as e:
            logging.error(f"Error moving file {file_name} to {target_folder}: {e}")

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
        del self.files[self.current_index]  # Remove the file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()

    def delete_marked_images(self) -> None:
        while self.actions_stack:
            action, *args = self.actions_stack.pop()
            if action == 'delete':
                file_name = args[0]
                file_path = os.path.join(self.folder_path, file_name)
                try:
                    os.remove(file_path)
                    logging.info(f"{file_name} deleted.")
                except Exception as e:
                    logging.error(f"Error deleting file {file_name}: {e}")

    def load_image(self) -> None:
        if not self.files:
            return

        try:
            file_name = self.files[self.current_index]
            file_path = os.path.join(self.folder_path, file_name)

            # Load image using PIL
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

    def undo_last_action(self) -> None:
        if not self.actions_stack:
            return

        action, *args = self.actions_stack.pop()
        if action == 'move':
            target_folder, file_name = args
            target_path = os.path.join(self.folder_path, target_folder, file_name)
            original_path = os.path.join(self.folder_path, file_name)
            try:
                shutil.move(target_path, original_path)
                logging.info(f"Undid move of {file_name} from '{target_folder}' back to original location.")
                self.files.insert(self.current_index, file_name)
                self.load_image()
            except Exception as e:
                logging.error(f"Error undoing move of file {file_name}: {e}")
        elif action == 'delete':
            file_name = args[0]
            self.files.insert(self.current_index, file_name)
            logging.info(f"Undid deletion of {file_name}.")
            self.load_image()

    def copy_image_to_special(self) -> None:
        if not self.files:
            return

        try:
            file_name = self.files[self.current_index]
            source_path = os.path.join(self.folder_path, file_name)
            special_folder_path = os.path.join(self.folder_path, '..', '..', 'Special')
            os.makedirs(special_folder_path, exist_ok=True)

            target_path = os.path.join(special_folder_path, file_name)
            shutil.copy2(source_path, target_path)

            logging.info(f"{file_name} copied to 'Special' folder.")
        except Exception as e:
            logging.error(f"Error copying file {file_name} to 'Special' folder: {e}")

    def move_image_to_lulz(self) -> None:
        if not self.files:
            return

        try:
            file_name = self.files[self.current_index]
            source_path = os.path.join(self.folder_path, file_name)
            lulz_folder_path = os.path.join(self.folder_path, '..', '..', 'lulz')
            os.makedirs(lulz_folder_path, exist_ok=True)

            target_path = os.path.join(lulz_folder_path, file_name)
            shutil.move(source_path, target_path)

            logging.info(f"{file_name} moved to 'lulz' folder.")
            self.actions_stack.append(('move', 'lulz', file_name))
            del self.files[self.current_index]  # Remove the moved file from the list

            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1 
            self.load_image()
        except Exception as e:
            logging.error(f"Error moving file {file_name} to 'lulz' folder: {e}")

    def move_image_to_tut(self) -> None:
        if not self.files:
            return

        try:
            file_name = self.files[self.current_index]
            source_path = os.path.join(self.folder_path, file_name)
            tut_folder_path = os.path.join(self.folder_path, '..', '..', 'tut')
            os.makedirs(tut_folder_path, exist_ok=True)

            target_path = os.path.join(tut_folder_path, file_name)
            shutil.move(source_path, target_path)

            logging.info(f"{file_name} moved to 'tut' folder.")
            self.actions_stack.append(('move', 'tut', file_name))
            del self.files[self.current_index]

            if self.current_index >= len(self.files):
                self.current_index = len(self.files) - 1

            self.load_image()
        except Exception as e:
            logging.error(f"Error moving file {file_name} to 'tut' folder: {e}")

def main() -> None:
    if len(sys.argv) != 2:
        logging.error("Usage: python3 qc.py /path/to/images")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        logging.error(f"The specified folder '{folder_path}' does not exist.")
        sys.exit(1)

    unzip_files(folder_path)

    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.png')
    ]

    viewer = ImageViewer(folder_path, files)
    viewer.mainloop()

    viewer.delete_marked_images()

if __name__ == "__main__":
    main()
