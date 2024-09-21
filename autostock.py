import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.font import Font
import subprocess
from GenerateCSV.categorias import categorias
import random
import json
import logging
from dotenv import load_dotenv
import threading
import queue
import glob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Get icon path from environment variables
ICON_PATH = "meulindo.ico"

SETTINGS_FILE = "settings.json"
accent_color_list = ["#800f00", "#004080", "#80005e", "#800000"]
accent_color = random.choice(accent_color_list)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

class SubprocessRunner:
    def __init__(self, command, output_queue):
        self.command = command
        self.output_queue = output_queue

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in iter(process.stdout.readline, ''):
                self.output_queue.put(line.strip())

            process.stdout.close()
            return_code = process.wait()

            if return_code != 0:
                self.output_queue.put(f"Command failed with return code {return_code}")
        except Exception as e:
            self.output_queue.put(f"Error running command: {str(e)}")

class AutostockGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Autostock Utils")
        self.master.geometry("300x900")
        self.master.configure(bg="#2b2b2b")
        self.master.wm_iconbitmap(ICON_PATH)

        self.bold_font = Font(family="Arial", size=12, weight="bold")
        self.small_font = Font(family="Arial", size=9)

        self.settings = load_settings()
        self.setup_ui()

        self.output_queue = queue.Queue()
        self.after_id = None
        self.check_output_queue()

    def setup_ui(self):
        # Folder selection
        self.folder_var = tk.StringVar(value=self.settings.get("folder_path", ""))
        tk.Label(self.master, text="Deixa eu fazer procê ❤️", bg="#2b2b2b", fg="#ffffff", font=self.bold_font).pack(pady=5)
        tk.Entry(self.master, textvariable=self.folder_var, width=16, bg="#4d4d4d", fg="#ffffff", font=("Arial", 20)).pack(pady=5)
        tk.Button(self.master, text="🔎", command=self.select_folder, bg=accent_color, fg="#ffffff", font=("Arial", 20)).pack(pady=20)

        # # Category selection
        # self.category_var = tk.StringVar(value=self.settings.get("selected_category", "Categoria"))
        # tk.OptionMenu(self.master, self.category_var, *categorias.values()).pack(pady=25)

        # QC Button
        tk.Button(self.master, text="🔬 QC", command=self.run_qc, bg=accent_color, width=12, height=2, fg="#ffffff").pack(pady=5)

        # Process checkboxes
        tk.Label(self.master, text="Quais processos?", bg="#2b2b2b", fg="#ffffff", font=self.bold_font).pack(pady=5)
        self.upscale_var = tk.BooleanVar(value=self.settings.get("selected_upscale", True))
        tk.Checkbutton(self.master, text="Upscale", variable=self.upscale_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)
        self.convert_to_jpg_var = tk.BooleanVar(value=self.settings.get("selected_convert_to_jpg", True))
        tk.Checkbutton(self.master, text="Convert to JPG", variable=self.convert_to_jpg_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)
        self.create_csv_var = tk.BooleanVar(value=self.settings.get("selected_create_csv", True))
        tk.Checkbutton(self.master, text="Generate CSV's", variable=self.create_csv_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)

        # Language selection
        tk.Label(self.master, text="Qual idioma pra adobe?", bg="#2b2b2b", fg="#ffffff", font=self.small_font).pack(pady=5)
        self.language_var = tk.StringVar(value=self.settings.get("selected_language", "en"))
        tk.OptionMenu(self.master, self.language_var, "pt", "en").pack(pady=5)

        # Platform selection
        tk.Label(self.master, text="Quais plataformas?", bg="#2b2b2b", fg="#ffffff", font=self.bold_font).pack(pady=5)
        self.adobe_var = tk.BooleanVar(value=self.settings.get("selected_adobe", True))
        tk.Checkbutton(self.master, text="Adobe", variable=self.adobe_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)
        self.freepik_var = tk.BooleanVar(value=self.settings.get("selected_freepik", True))
        tk.Checkbutton(self.master, text="Freepik", variable=self.freepik_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)
        self.dreamstime_var = tk.BooleanVar(value=self.settings.get("selected_dreamstime", True))
        tk.Checkbutton(self.master, text="Dreamstime", variable=self.dreamstime_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)
        self.RF_var = tk.BooleanVar(value=self.settings.get("selected_rf", True))
        tk.Checkbutton(self.master, text="123RF", variable=self.RF_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color).pack(pady=5)

        # Process button
        tk.Button(
        self.master, text="🚀", 
        command=lambda: threading.Thread(target=self.process_workflow_thread).start(),
        bg=accent_color, 
        fg="#ffffff", 
        width=15, 
        height=3, 
        font=("Arial", 20)).pack(pady=50)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_var.set(folder_selected)

    def run_command(self, command):
        """Run a command synchronously."""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in iter(process.stdout.readline, ''):
                logging.info(line.strip())

            process.stdout.close()
            return_code = process.wait()

            if return_code != 0:
                logging.error(f"Command failed with return code {return_code}")
        except Exception as e:
            logging.error(f"Error running command: {str(e)}")

    def check_output_queue(self):
        try:
            while True:
                output = self.output_queue.get_nowait()
                logging.info(output)
        except queue.Empty:
            pass
        finally:
            self.after_id = self.master.after(100, self.check_output_queue)

    def run_qc(self):
        folder_path = self.folder_var.get()
        if not folder_path:
            messagebox.showerror("Error", "A gente precisa de uma pasta bebê.")
            return

        self.run_command(f"python qc/qc.py {folder_path}")

        if os.path.exists(os.path.join(folder_path, "letterbox")):
            self.run_command(f"python Utils/organize_images.py {os.path.join(folder_path, 'letterbox')}")

        self.save_current_settings()

    def process_workflow_thread(self):
        """Run the workflow on a separate thread to keep the GUI responsive."""
        # Disable UI elements during processing
        self.disable_ui()

        # Run the actual workflow
        try:
            self.process_workflow()
        finally:
            # Re-enable UI elements after processing
            self.enable_ui()

    def process_workflow(self):
        folder_path = self.folder_var.get()
        if not folder_path:
            messagebox.showerror("Error", "A gente precisa de uma pasta bebê.")
            return

        # selected_category = self.category_var.get()
        # if selected_category == "Categoria":
        #     messagebox.showerror("Error", "A gente precisa de uma categoria bebê.")
        #     return

        self.save_current_settings()

        # Move files from letterbox if it exists
        if os.path.exists(os.path.join(folder_path, "letterbox")):
            self.move_and_delete_files(folder_path)

        platforms = ""

        if self.freepik_var.get():
            platforms += " f "
        if self.adobe_var.get():
            platforms += " a "
        if self.dreamstime_var.get():
            platforms += " d "
        if self.RF_var.get():
            platforms += " r "

        # Step 1: Upscale images
        if self.upscale_var.get():
            self.upscale(folder_path)

        # Step 2: Convert images to JPEG
        if self.convert_to_jpg_var.get():
            self.convert_to_jpg(folder_path)

         # Step 3: Create CSVs for all selected platforms
        if self.create_csv_var.get() and platforms:
            self.create_csv(folder_path, platforms, self.language_var.get())

        # Step 4: Add quotes to the Freepik CSV
        if self.freepik_var.get():
            self.add_quotes_to_csv(folder_path)


    def disable_ui(self):
        """Disable UI elements to prevent interaction during processing."""
        # self.master.config(cursor="wait")
        for widget in self.master.winfo_children():
            widget.config(state=tk.DISABLED)

    def enable_ui(self):
        """Enable UI elements after processing is complete."""
        self.master.config(cursor="")
        for widget in self.master.winfo_children():
            widget.config(state=tk.NORMAL)

    def upscale(self, folder_path):
        self.run_command(f"python Utils/upscale.py {folder_path}")

    def convert_to_jpg(self, folder_path):
        png_folder = os.path.join(folder_path, "realesrgan")
        self.run_command(f"python Utils/convertToJPG.py {png_folder}")

    def create_csv(self, folder_path, platforms, language):
        self.run_command(f"python generateCSV/generateCSV.py {folder_path} -p {platforms} --language {language}")

    def add_quotes_to_csv(self, folder_path):
        freepik_csv_files = glob.glob(os.path.join(folder_path, "*_freepik.csv"))
        if freepik_csv_files:
            for csv_file in freepik_csv_files:
                self.run_command(f'python ./Utils/addQuotesToCSV.py "{csv_file}"')
                logging.info(f"Added quotes to CSV: {csv_file}")
            
    def move_and_delete_files(self, folder_path):
        letterbox_folder = os.path.join(folder_path, "letterbox")
        if os.path.exists(letterbox_folder):
            for root, dirs, files in os.walk(letterbox_folder):
                for dir_name in list(dirs):
                    dir_path = os.path.join(root, dir_name)
                    if dir_name.lower() == "jpeg":
                        shutil.rmtree(dir_path)
                        dirs.remove(dir_name)
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.lower().endswith(".jpg"):
                        os.remove(file_path)
                    else:
                        shutil.move(file_path, os.path.join(folder_path, file))
            shutil.rmtree(letterbox_folder)

    def save_current_settings(self):
        settings = {
            "folder_path": self.folder_var.get(),
            # "selected_category": self.category_var.get(),
            "selected_upscale": self.upscale_var.get(),
            "selected_convert_to_jpg": self.convert_to_jpg_var.get(),
            "selected_create_csv": self.create_csv_var.get(),
            "selected_language": self.language_var.get(),
            "selected_adobe": self.adobe_var.get(),
            "selected_freepik": self.freepik_var.get(),
            "selected_dreamstime": self.dreamstime_var.get(),
            "selected_RF": self.RF_var.get(),
        }
        save_settings(settings)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutostockGUI(root)
    root.mainloop()