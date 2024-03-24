import os
import sys
import shutil
import tkinter as tk
from PIL import Image, ImageTk

# Dark mode stylesheet
dark_stylesheet = """
    .viewer {
        background-color: #2b2b2b;
        color: #f0f0f0;
    }
"""

class ImageViewer(tk.Tk):
    def __init__(self, folder_path, files):
        super().__init__()

        self.folder_path = folder_path
        self.files = files
        self.current_index = 0

        self.title("Image Viewer")
        self.geometry("800x600")
        self.configure(background="#2b2b2b")

        # Set window icon
        icon_path = os.path.join(sys.path[0], '..', 'meulindo.ico')  # Assuming icon.ico is one directory up
        self.iconbitmap(icon_path)


        self.viewer = tk.Label(self, bg="#2b2b2b")
        self.viewer.pack(expand=True, fill="both")

        self.load_image()

        self.bind("<Right>", lambda event: self.next_image())
        self.bind("<Left>", lambda event: self.previous_image())
        self.bind("<Key-x>", lambda event: self.delete_image())
        self.bind("<Key-q>", lambda event: sys.exit())
        self.bind("<Key-w>", lambda event: self.move_image_to_folder("watermark"))
        self.bind("<Key-b>", lambda event: self.move_image_to_folder("letterbox"))

    def move_image_to_folder(self, target_folder):
        if not self.files:
            return

        file_name = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, file_name)
        target_folder_path = os.path.join(self.folder_path, target_folder)

        os.makedirs(target_folder_path, exist_ok=True)

        target_path = os.path.join(target_folder_path, file_name)

        shutil.move(source_path, target_path)

        print(f"{file_name} moved to '{target_folder}' folder.")
        del self.files[self.current_index]  # Remove the moved file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.files)
        self.load_image()

    def previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.files)
        self.load_image()

    def delete_image(self):
        if not self.files:
            return

        file_path = os.path.join(self.folder_path, self.files[self.current_index])
        os.remove(file_path)
        print(f"{self.files[self.current_index]} deleted.")
        del self.files[self.current_index]  # Remove the deleted file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()

    def load_image(self):
        if not self.files:
            return

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

        # Set window title with current file index
        self.title(f"{file_name} - {self.current_index + 1}/{len(self.files)}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 qc.py /path/to/images")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"The specified folder '{folder_path}' does not exist.")
        sys.exit(1)

    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    viewer = ImageViewer(folder_path, files)

    viewer.mainloop()
