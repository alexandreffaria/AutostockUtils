import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
import subprocess
from GenerateCSV.categorias import categorias
import random
import json
import logging
from dotenv import load_dotenv
import threading

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Get icon path from environment variables
ICON_PATH = "meulindo.ico"

SETTINGS_FILE = "settings.json"
accent_color_list = ["#800f00", "#004080", "#80005e", "#800000"]
accent_color = random.choice(accent_color_list)


def load_settings() -> dict:
    """
    Load settings from the JSON file.
    """
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            logging.info("Settings loaded successfully.")
            return settings
    logging.warning("Settings file not found.")
    return {}


def save_settings(settings: dict) -> None:
    """
    Save settings to the JSON file.
    """
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
        logging.info("Settings saved successfully.")



def run_command(command):
    try:
        logging.info(f"Running command: {command}")

        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        # Log stdout and stderr for debugging purposes
        if result.stdout:
            logging.info(result.stdout.strip())
        if result.stderr:
            logging.error(result.stderr.strip())

        # Check if the command was successful
        result.check_returncode()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def show_custom_error(message: str) -> None:
    """
    Show a custom error message in a tkinter window.
    """
    error_window = tk.Toplevel(root)
    error_window.configure(bg="#2b2b2b")
    error_window.title("Cadê?!")
    error_window.wm_iconbitmap(ICON_PATH)
    error_label = tk.Label(error_window, text=message, bg="#2b2b2b", fg="#ffffff")
    error_label.pack(padx=20, pady=10)
    ok_button = tk.Button(error_window, text="Desculpe meu senhor", command=error_window.destroy, bg=accent_color, fg="#ffffff")
    ok_button.pack(pady=10, padx=20)
    logging.error(message)


def upscale(folder_path: str) -> None:
    """
    Run the upscale script.
    """
    command = f"python Utils/upscale.py {folder_path}"
    run_command(command)


def convert_to_jpg(folder_path: str) -> None:
    """
    Run the convertToJPG script.
    """
    png_folder = folder_path + "/realesrgan/"
    command = f"python Utils/convertToJPG.py {png_folder}"
    run_command(command)


def create_csv(folder_path: str, selected_category: str, platform: str, no_prompt: bool, language: str) -> None:
    """
    Run the generateCSV script.
    """
    prompt_flag = "--no-prompt" if no_prompt else ""
    command = f"python generateCSV/generateCSV.py {folder_path}/ \"{selected_category}\" -p {platform[0].lower()} {prompt_flag} --language {language}"
    run_command(command)


def upload(folder_path: str, platform: str) -> None:
    """
    Run the sendSFTP script.
    """
    command = f"python Utils/sendSFTP.py {folder_path}/ {platform[0].lower()}"
    run_command(command)


def process_workflow() -> None:
    """
    Execute the selected workflow.
    """
    logging.debug("Process button clicked.")
    selected_adobe = adobe_var.get()
    selected_freepik = freepik_var.get()
    selected_upscale = upscale_var.get()
    selected_convert_to_jpg = convert_to_jpg_var.get()
    selected_create_csv = create_csv_var.get()
    selected_upload = upload_var.get()
    selected_no_prompt = no_prompt_var.get()
    selected_language = language_var.get()
    folder_path = folder_var.get()
    selected_category = category_var.get()

    logging.debug(f"Selected Adobe: {selected_adobe}, Selected Freepik: {selected_freepik}, "
                  f"Selected Upscale: {selected_upscale}, Selected Convert to JPG: {selected_convert_to_jpg}, "
                  f"Selected Create CSV: {selected_create_csv}, Selected Upload: {selected_upload}, "
                  f"Selected No Prompt: {selected_no_prompt}, Selected Language: {selected_language}, "
                  f"Folder Path: {folder_path}, Selected Category: {selected_category}")

    settings = {
        "folder_path": folder_path,
        "selected_category": selected_category,
        "selected_adobe": selected_adobe,
        "selected_freepik": selected_freepik,
        "selected_upscale": selected_upscale,
        "selected_convert_to_jpg": selected_convert_to_jpg,
        "selected_create_csv": selected_create_csv,
        "selected_upload": selected_upload,
        "selected_no_prompt": selected_no_prompt,
        "selected_language": selected_language,
    }
    save_settings(settings)

    if not folder_path:
        show_custom_error("A gente precisa de uma pasta bebê.")
        return

    if selected_category == "Categoria":
        show_custom_error("A gente precisa de uma categoria bebê.")
        return

    # If there is a folder called letterbox, move all files from all subfolders to the folderpath folder
    if os.path.exists(folder_path + "/letterbox/"):
        move_and_delete_files(folder_path)

    def run_tasks():
        logging.debug("Running tasks...")
        if selected_adobe:
            if selected_upscale:
                logging.debug("Upscaling images for Adobe.")
                upscale(folder_path)
            if selected_create_csv:
                logging.debug("Creating CSV for Adobe.")
                create_csv(folder_path, selected_category, "a", selected_no_prompt, selected_language)
            if selected_upload:
                logging.debug("Uploading files to Adobe.")
                upload(folder_path, "Adobe")

        if selected_freepik:
            if selected_convert_to_jpg:
                logging.debug("Converting images to JPG for Freepik.")
                convert_to_jpg(folder_path)
            if selected_create_csv:
                logging.debug("Creating CSV for Freepik.")
                create_csv(folder_path, selected_category, "f", selected_no_prompt, "en")
            if selected_upload:
                logging.debug("Uploading files to Freepik.")
                upload(folder_path, "Freepik")

    threading.Thread(target=run_tasks).start()


def move_and_delete_files(folder_path):
    letterbox_folder = os.path.join(folder_path, "letterbox")

    if os.path.exists(letterbox_folder):
        for root, dirs, files in os.walk(letterbox_folder):
            # Check and delete JPEG folders immediately
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if dir_name.lower() == "jpeg":
                    shutil.rmtree(dir_path)
                    print(f"Deleted JPEG directory and its contents: {dir_path}")

            for file in files:
                file_path = os.path.join(root, file)
                # Skip .jpg files
                if file.lower().endswith(".jpg"):
                    os.remove(file_path)
                    print(f"Deleted .jpg file: {file_path}")
                else:
                    target_file_path = os.path.join(folder_path, file)
                    shutil.move(file_path, target_file_path)
                    print(f"Moved {file_path} to {target_file_path}")

        # Remove empty directories
        for root, dirs, files in os.walk(letterbox_folder, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):  # Check if the directory is empty
                    os.rmdir(dir_path)
                    print(f"Deleted empty directory: {dir_path}")

        # Finally, delete the letterbox folder itself
        shutil.rmtree(letterbox_folder)
        print(f"Deleted the letterbox directory: {letterbox_folder}")


def select_folder() -> None:
    """
    Open a file dialog to select a folder.
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        root.configure(bg="#2b2b2b")


def run_qc() -> None:
    """
    Run the qc.py script.
    """
    folder_path = folder_var.get()
    if not folder_path:
        show_custom_error("A gente precisa de uma pasta bebê.")
        return

    save_settings({
        "folder_path": folder_path
    })

    command = f"python Utils/qc.py {folder_path}"
    run_command(command)

    if os.path.exists(folder_path + "/letterbox/"):
               run_command(f"python Utils/organize_images.py {folder_path}/letterbox/")

    save_settings(load_settings())  # Save settings after running qc.py


# Main window
root = tk.Tk()
root.title("Autostock Utils")
root.geometry("300x900")
root.configure(bg="#2b2b2b")
root.wm_title("Autostock Utils")
root.wm_iconbitmap(ICON_PATH)

bold_font = Font(family="Arial", size=12, weight="bold")
small_font = Font(family="Arial", size=9)

settings = load_settings()

# Folder selection
folder_var = tk.StringVar(value=settings.get("folder_path", ""))
folder_label = tk.Label(root, text="Deixa eu fazer procê ❤️", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
folder_label.pack(pady=5, padx=20)

folder_entry = tk.Entry(root, textvariable=folder_var, width=16, bg="#4d4d4d", fg="#ffffff", font=("Arial", 20))
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="🔎", command=select_folder, bg=accent_color, fg="#ffffff", font=("Arial", 20))
folder_button.pack(pady=20)

# Category selection
category_var = tk.StringVar(value=settings.get("selected_category", "Categoria"))
category_menu = tk.Menu(root, bg="#4d4d4d", fg="#ffffff")
root.config(menu=category_menu)

category_optionmenu = tk.OptionMenu(root, category_var, *categorias.values())
category_optionmenu["menu"].config(bg="#4d4d4d", fg="#ffffff")
category_optionmenu.config(bg="#4d4d4d", fg="#ffffff")
category_optionmenu.pack(pady=25)
category_optionmenu.config(highlightthickness=1, highlightbackground=accent_color)

# Button to run QC separately
qc_button = tk.Button(root, text="🔬 QC", command=run_qc, bg=accent_color, width=12, height=2, fg="#ffffff")
qc_button.pack(pady=5)

process_labels = tk.Label(root, text="Quais processos?", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
process_labels.pack(pady=5, padx=20)

upscale_var = tk.BooleanVar(value=settings.get("selected_upscale", True))
upscale_checkbox = tk.Checkbutton(root, text="Upscale", variable=upscale_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color, activebackground="#2b2b2b", activeforeground="#fff")
upscale_checkbox.pack(pady=5)

convert_to_jpg_var = tk.BooleanVar(value=settings.get("selected_convert_to_jpg", True))
convert_to_jpg_checkbox = tk.Checkbutton(root, text="Convert to JPG", variable=convert_to_jpg_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color, activebackground="#2b2b2b", activeforeground="#fff")
convert_to_jpg_checkbox.pack(pady=5)

create_csv_var = tk.BooleanVar(value=settings.get("selected_create_csv", True))
create_csv_checkbox = tk.Checkbutton(root, text="Generate CSV's", variable=create_csv_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color, activebackground="#2b2b2b", activeforeground="#fff")
create_csv_checkbox.pack(pady=5)

upload_var = tk.BooleanVar(value=settings.get("selected_upload", False))

no_prompt_var = tk.BooleanVar(value=settings.get("selected_no_prompt", False))

platform_labels = tk.Label(root, text="Qual idioma pra adobe?", bg="#2b2b2b", fg="#ffffff", font=small_font, height=1)
platform_labels.pack(pady=5, padx=20)

language_var = tk.StringVar(value=settings.get("selected_language", "en"))
language_menu = tk.OptionMenu(root, language_var, "pt", "en")
language_menu.config(bg="#4d4d4d", fg="#ffffff")
language_menu.pack(pady=5)
language_menu.config(highlightthickness=1, highlightbackground=accent_color)

platform_labels = tk.Label(root, text="Quais plataformas?", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
platform_labels.pack(pady=5, padx=20)

adobe_var = tk.BooleanVar(value=settings.get("selected_adobe", True))
adobe_checkbox = tk.Checkbutton(root, text="Adobe", variable=adobe_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color, activebackground="#2b2b2b", activeforeground="#fff")
adobe_checkbox.pack(pady=5)

freepik_var = tk.BooleanVar(value=settings.get("selected_freepik", True))
freepik_checkbox = tk.Checkbutton(root, text="Freepik", variable=freepik_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color, activebackground="#2b2b2b", activeforeground="#fff")
freepik_checkbox.pack(pady=5)

# Process button
process_button = tk.Button(root, text="🚀", command=process_workflow, bg=accent_color, fg="#ffffff", width=15, height=3, font=("Arial", 20))
process_button.pack(pady=50)

root.mainloop()
