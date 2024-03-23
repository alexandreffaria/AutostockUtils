import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from subprocess import Popen, PIPE
from GenerateCSV.categorias import categorias

# Function to run a shell command and report progress in GUI
def run_command(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
       

# Function to execute the workflow
def process_workflow():
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder first.")
        return
    
    selected_category = category_var.get()  
    selected_adobe = adobe_var.get() 
    selected_vecteezy = vecteezy_var.get() 

    command = f"python Utils/qc.py {folder_path}"  # Enclose folder path in quotes
    run_command(command)

    # Check if folder exists to avoid running upscale.py without a valid path
    if os.path.exists(folder_path):
        command = f"python Utils/upscale.py {folder_path}"  # Enclose folder path in quotes
        run_command(command)

    png_folder = folder_path + "/realesrgan/"

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
root.geometry("600x400")
root.configure(bg="#2b2b2b")
# Center the window title
root.wm_title(" " * 75 + "Autostock Utils")

root.wm_iconbitmap('meulindo.ico')

# Folder selection
folder_var = tk.StringVar()
folder_label = tk.Label(root, text="Cade as fota?", bg="#2b2b2b", fg="#ffffff")
folder_label.pack(pady=5)
folder_entry = tk.Entry(root, textvariable=folder_var, width=50, bg="#4d4d4d", fg="#ffffff")  # Adjust background and foreground colors
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="Pasta das fota", command=select_folder, bg="#004080", fg="#ffffff")
folder_button.pack(pady=5)

# Category selection
category_var = tk.StringVar()
category_var.set("Categoria")
category_label = tk.Label(root, text="Qual é a categoria?", bg="#2b2b2b", fg="#ffffff")
category_label.pack(pady=5)

category_menu = tk.Menu(root, bg="#4d4d4d", fg="#ffffff")  # Configure the background and foreground colors for the dropdown menu
root.config(menu=category_menu)

category_optionmenu = tk.OptionMenu(root, category_var, *categorias.values())
category_optionmenu["menu"].config(bg="#4d4d4d", fg="#ffffff")  # Configure the background and foreground colors for the dropdown menu
category_optionmenu.config(bg="#4d4d4d", fg="#ffffff")  # Adjust background and foreground colors
category_optionmenu.pack(pady=5)

# Checkbox for Adobe
adobe_var = tk.BooleanVar(value=True)  # Set Adobe checkbox initially checked
adobe_checkbox = tk.Checkbutton(root, text="Adobe", variable=adobe_var, bg="#2b2b2b", fg="#ffffff", selectcolor="#004080",activebackground="#2b2b2b", activeforeground="#fff" )
adobe_checkbox.pack(pady=5)

# Checkbox for Vecteezy
vecteezy_var = tk.BooleanVar(value=True)  # Set Vecteezy checkbox initially checked
vecteezy_checkbox = tk.Checkbutton(root, text="Vecteezy", variable=vecteezy_var, bg="#2b2b2b", fg="#ffffff", selectcolor="#004080",activebackground="#2b2b2b", activeforeground="#fff")
vecteezy_checkbox.pack(pady=5)

# Process button
process_button = tk.Button(root, text="BORAAA", command=process_workflow, bg="#004080", fg="#ffffff", width=16, height=3)
process_button.pack(pady=50)

root.mainloop()
