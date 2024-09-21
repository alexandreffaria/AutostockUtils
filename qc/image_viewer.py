import os
import tkinter as tk
from PIL import Image, ImageTk
import logging
from typing import List, Dict

from constants import (
    ICON_PATH, ACTION_KEEP, KEY_NEXT, KEY_PREV, KEY_DELETE, KEY_QUIT,
    KEY_UNDO, KEY_SPECIAL, KEY_LULZ, KEY_TUT
)
from action_handlers import (
    mark_image_for_deletion, move_image_to_folder, copy_image_to_special,
    move_to_lulz, move_to_tut
)
from record_management import write_state_file, write_record_file, merge_records_to_master_csv
from file_operations import remove_file

class ImageViewer(tk.Tk):
    SHIFT_MASK = 0x0001  # Mask for the Shift key in event.state

    def __init__(self, folder_path: str, files: List[str], last_image: str = '', existing_records: Dict[str, str] = {}):
        super().__init__()

        self.folder_path = folder_path
        self.files = files
        self.current_index = 0
        self.actions_stack = []
        self.record_entries = existing_records.copy()

        self.setup_ui()
        self.bind_keys()

        # Set current index based on last viewed image
        if last_image:
            try:
                self.current_index = self.files.index(last_image)
            except ValueError:
                logging.warning(f"Last viewed image '{last_image}' not found. Starting from the first image.")
                self.current_index = 0

        self.load_image()

    def setup_ui(self):
        self.title("Image Viewer")
        self.geometry("800x600")
        self.configure(background="#2b2b2b")
        self.iconbitmap(ICON_PATH)

        self.viewer = tk.Label(self, bg="#2b2b2b")
        self.viewer.pack(expand=True, fill="both")

        # Bind the window close event
        self.protocol("WM_DELETE_WINDOW", self.close_viewer)

    def bind_keys(self):
        self.bind(KEY_NEXT, self.on_move)
        self.bind(KEY_PREV, self.on_move)
        self.bind("<Key-h>", lambda event: self.on_move(event, -1))
        self.bind("<Key-l>", lambda event: self.on_move(event, 1))
        self.bind(KEY_DELETE, lambda event: self.mark_image_for_deletion())
        self.bind("<Control_R>", lambda event: self.mark_image_for_deletion())
        self.bind(KEY_QUIT, lambda event: self.close_viewer())
        self.bind("<Key-w>", lambda event: self.move_image_to_folder("watermark"))
        self.bind("<Key-b>", lambda event: self.move_image_to_folder("letterbox"))
        self.bind("<Key-/>", lambda event: self.move_image_to_folder("letterbox"))
        self.bind(KEY_UNDO, lambda event: self.undo_last_action())
        self.bind(KEY_SPECIAL, lambda event: self.copy_image_to_special())
        self.bind(KEY_LULZ, lambda event: self.move_image_to_lulz())
        self.bind(KEY_TUT, lambda event: self.move_image_to_tut())

        # Bind mouse wheel event
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<Button-4>", self.on_mouse_wheel)  # For Linux systems
        self.bind("<Button-5>", self.on_mouse_wheel)  # For Linux systems

    def on_move(self, event, direction=None):
        if direction is None:
            direction = 1 if event.keysym == "Right" else -1
        
        shift_held = event.state & self.SHIFT_MASK
        step = 10 if shift_held else 1
        
        self.shift_images(direction * step)

    def shift_images(self, step: int) -> None:
        self.record_current_image_if_not_recorded()
        new_index = max(0, min(len(self.files) - 1, self.current_index + step))
        if new_index != self.current_index:
            self.current_index = new_index
            self.load_image()

    def on_mouse_wheel(self, event):
        if hasattr(event, 'delta'):
            direction = -1 if event.delta > 0 else 1
        else:
            # For Linux systems
            direction = -1 if event.num == 4 else 1
        self.on_move(event, direction)

    def close_viewer(self):
        self.record_current_image_if_not_recorded()

        last_image = self.files[self.current_index] if self.files else ''
        state_file_path = os.path.join(self.folder_path, 'qc_state.txt')
        write_state_file(state_file_path, last_image)

        record_file_path = os.path.join(self.folder_path, 'qc_record.txt')
        write_record_file(self.record_entries, record_file_path)

        merge_records_to_master_csv(self.folder_path, self.record_entries)

        self.process_deletions_at_end()

        self.destroy()

    def process_deletions_at_end(self):
        for file_name, action in self.record_entries.items():
            if action == ACTION_KEEP:
                file_path = os.path.join(self.folder_path, file_name)
                if os.path.exists(file_path):
                    try:
                        remove_file(file_path)
                        logging.info(f"{file_name} deleted upon closing the viewer.")
                    except Exception as e:
                        logging.error(f"Error deleting file {file_name}: {e}")

    def record_current_image_if_not_recorded(self):
        if self.files:
            file_name = self.files[self.current_index]
            if file_name not in self.record_entries:
                self.record_entries[file_name] = ACTION_KEEP

    def mark_image_for_deletion(self) -> None:
        if not self.files:
            return
        file_name = self.files[self.current_index]
        self.current_index = mark_image_for_deletion(file_name, self.current_index, self.files, self.actions_stack, self.record_entries)
        self.load_image()

    def move_image_to_folder(self, target_folder: str) -> None:
        if not self.files:
            return
        file_name = self.files[self.current_index]
        self.current_index = move_image_to_folder(file_name, self.current_index, self.files, self.actions_stack, self.record_entries, self.folder_path, target_folder)
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
                self.shift_images(1)  # Try loading the next image
            else:
                self.viewer.configure(image='')
                self.viewer.image = None
                self.title("Image Viewer")

    def undo_last_action(self) -> None:
        if not self.actions_stack:
            return

        action, *args = self.actions_stack.pop()
        file_name = args[-1]

        if action == ACTION_KEEP:
            # Move the file back to its original location
            source_folder = args[0]
            source_path = os.path.join(self.folder_path, source_folder, file_name)
            target_path = os.path.join(self.folder_path, file_name)
            try:
                os.rename(source_path, target_path)
                logging.info(f"Undid move of {file_name} from '{source_folder}' back to original location.")
                self.files.insert(self.current_index, file_name)
                if self.record_entries.get(file_name) == source_folder:
                    del self.record_entries[file_name]
                self.load_image()
            except Exception as e:
                logging.error(f"Error undoing move of file {file_name}: {e}")
        elif action == ACTION_KEEP:
            self.files.insert(self.current_index, file_name)
            logging.info(f"Undid deletion of {file_name}.")
            if self.record_entries.get(file_name) == ACTION_KEEP:
                del self.record_entries[file_name]
            self.load_image()

    def copy_image_to_special(self) -> None:
        if not self.files:
            return
        file_name = self.files[self.current_index]
        copy_image_to_special(file_name, self.folder_path)

    def move_image_to_lulz(self) -> None:
        if not self.files:
            return
        file_name = self.files[self.current_index]
        self.current_index = move_to_lulz(file_name, self.current_index, self.files, self.actions_stack, self.record_entries, self.folder_path)
        self.load_image()

    def move_image_to_tut(self) -> None:
        if not self.files:
            return
        file_name = self.files[self.current_index]
        self.current_index = move_to_tut(file_name, self.current_index, self.files, self.actions_stack, self.record_entries, self.folder_path)
        self.load_image()