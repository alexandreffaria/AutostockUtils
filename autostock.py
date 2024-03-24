import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from subprocess import Popen, PIPE
from GenerateCSV.categorias import categorias
import random

accent_color_list = ["#800f00", "#004080", "#80005e", "#800000"]
accent_color = random.choice(accent_color_list)

# Function to run a shell command Function to run a shell command
def run_command(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error: Command '{command}' failed with return code {process.returncode}")
        if stdout:
            print("stdout:")
            print(stdout)
        if stderr:
            print("stderr:")
            print(stderr)

def show_custom_error(message):
    error_window = tk.Toplevel(root)
    error_window.configure(bg="#2b2b2b")
    error_window.title("Cadê?!")
    error_window.wm_iconbitmap('meulindo.ico')
    error_label = tk.Label(error_window, text=message, bg="#2b2b2b", fg="#ffffff")
    error_label.pack(padx=20, pady=10)
    ok_button = tk.Button(error_window, text="Desculpe meu senhor", command=error_window.destroy, bg=accent_color, fg="#ffffff")
    ok_button.pack(pady=10, padx=20)

# Function to execute the workflow
def process_workflow():
    folder_path = folder_var.get()
    if not folder_path:
        show_custom_error("A gente precisa de uma pasta bebê.")
        return
    
    selected_category = category_var.get()  
    selected_adobe = adobe_var.get() 
    selected_vecteezy = vecteezy_var.get() 

    # Check if a category has been selected
    if selected_category == "Categoria":
        show_custom_error("A gente precisa de uma categoria bebê.")
        return

    command = f"python Utils/qc.py {folder_path}"  # Enclose folder path in quotes
    run_command(command)

    # Check if folder exists to avoid running upscale.py without a valid path
    if os.path.exists(folder_path):
        command = f"python Utils/upscale.py {folder_path}"  # Enclose folder path in quotes
        run_command(command)

    png_folder = folder_path + "/realesrgan/"
    if selected_vecteezy:
        if os.path.exists(png_folder):
            command = f"python Utils/convertToJPG.py {png_folder}"  # Enclose folder path in quotes
            run_command(command)

    if selected_adobe:
        command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/ \"{selected_category}\" -p a" 
        run_command(command)

    if selected_vecteezy:
        command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/jpgs/ \"{selected_category}\" -p v" 
        run_command(command)

    if selected_adobe:
        command = f"python Utils/sendSFTP.py {folder_path}/realesrgan/ -p a" 
        run_command(command)

    if selected_vecteezy:
        command = f"python Utils/sendSFTP.py {folder_path}/realesrgan/jpgs/ -p v" 
        run_command(command)

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        root.configure(bg="#2b2b2b")
        

# Main window
root = tk.Tk()
root.title("Autostock Utils")
root.geometry("300x500")
root.configure(bg="#2b2b2b")
# Center the window title
root.wm_title("Autostock Utils")

root.wm_iconbitmap('meulindo.ico')

bold_font = Font(family="Arial", size=12, weight="bold")

# Folder selection
folder_var = tk.StringVar()
folder_label = tk.Label(root,text="Deixa eu fazer procê ❤️", bg="#2b2b2b", fg="#ffffff", font=bold_font, height=1)
folder_label.pack(pady=5, padx=20)

folder_entry = tk.Entry(root, textvariable=folder_var, width=16, bg="#4d4d4d", fg="#ffffff", font=("Arial", 20))  # Adjust background and foreground colors
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="🔎", command=select_folder, bg=accent_color, fg="#ffffff", font=("Arial", 20))
folder_button.pack(pady=20)

# Category selection
category_var = tk.StringVar()
category_var.set("Categoria")

category_menu = tk.Menu(root, bg="#4d4d4d", fg="#ffffff")  # Configure the background and foreground colors for the dropdown menu
root.config(menu=category_menu)

category_optionmenu = tk.OptionMenu(root, category_var, *categorias.values())
category_optionmenu["menu"].config(bg="#4d4d4d", fg="#ffffff")  # Configure the background and foreground colors for the dropdown menu
category_optionmenu.config(bg="#4d4d4d", fg="#ffffff")  # Adjust background and foreground colors
category_optionmenu.pack(pady=25)

category_optionmenu.config(highlightthickness=1, highlightbackground=accent_color) 

# Checkbox for Adobe
adobe_var = tk.BooleanVar(value=True)  # Set Adobe checkbox initially checked
adobe_checkbox = tk.Checkbutton(root, text="Adobe", variable=adobe_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff" )
adobe_checkbox.pack(pady=5)

# Checkbox for Vecteezy
vecteezy_var = tk.BooleanVar(value=True)  # Set Vecteezy checkbox initially checked
vecteezy_checkbox = tk.Checkbutton(root, text="Vecteezy", variable=vecteezy_var, bg="#2b2b2b", fg="#ffffff", selectcolor=accent_color,activebackground="#2b2b2b", activeforeground="#fff")
vecteezy_checkbox.pack(pady=5)

# Process button
process_button = tk.Button(root, text="🚀", command=process_workflow, bg=accent_color, fg="#ffffff", width=15, height=3, font=("Arial", 20))
process_button.pack(pady=50)

root.mainloop()
