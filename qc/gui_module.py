import tkinter as tk
from PIL import Image, ImageTk
from typing import List, Dict, Tuple, Callable, Set, Any
from styles import get_dark_mode_styles

KeyBindingsType = Dict[Tuple[str, ...], Callable[[tk.Event], None]]

class ImageViewer:
    def __init__(
            self, 
            image_paths: List[str], 
            key_bindings: KeyBindingsType, 
            processed_images: Dict[str, Set[str]],
            start_index: int = 0
            ) -> None:

        self.deleted_images = processed_images['deleted']
        self.letterbox_images = processed_images['letterbox']
        self.undo_stack: List[Dict[str, Any]] = []

        self.root: tk.Tk = tk.Tk()
        self.root.title("QC")

        styles = get_dark_mode_styles()
        self.root.configure(bg=styles['background'])

        self.image_paths = image_paths
        self.key_bindings = key_bindings
        self.current_index = start_index

        if self.current_index >= len(self.image_paths):
            self.current_index = 0

        self.label = tk.Label(
            self.root,
            bg=styles['label']['bg'],
            fg=styles['label']['fg']
        )
        self.label.pack(expand=True, fill=tk.BOTH)

        if self.image_paths:
            self.display_image(self.current_index)
        else:
            tk.messagebox.showinfo("Info", "No images to display.")
            self.root.destroy()

        self.bind_keys()
        self.root.bind('<Configure>', self.on_resize)
        self.root.geometry("800x600")  # Set initial window size

    def _resize_image(self, pil_image: Image.Image, max_width: int, max_height: int) -> ImageTk.PhotoImage:
        """
        Resizes the image to fit within the specified max width and height, maintaining aspect ratio.
        """
        pil_image.thumbnail((max_width, max_height), Image.LANCZOS)
        return ImageTk.PhotoImage(pil_image)

    def display_image(self, index: int) -> None:
        image_path: str = self.image_paths[index]
        pil_image: Image.Image = Image.open(image_path)

        # Get the current window size
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        tk_image = self._resize_image(pil_image, window_width, window_height)
        self.label.configure(image=tk_image)
        self.label.image = tk_image  # Keep a reference to prevent garbage collection

        # Add the first 20 characters of the file name to the title
        short_file_name = image_path.split('/')[-1][17:90]
        self.root.title(f"QC ({index + 1}/{len(self.image_paths)}) - {short_file_name}")

    def bind_keys(self) -> None:
        for keys, function in self.key_bindings.items():
            for key in keys:
                self.root.bind(key, function)

    def next_image(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.display_image(self.current_index)

    def previous_image(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.display_image(self.current_index)

    def start(self) -> None:
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self) -> None:
        self.root.quit()

    def on_resize(self, event) -> None:
        self.display_image(self.current_index)