import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from subprocess import Popen, PIPE
from GenerateCSV.categorias import categorias

# Function to run a shell command and report progress in GUI
def run_command(command, progress_text):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            progress_text.insert(tk.END, output + '\n')
            progress_text.see(tk.END)
            progress_text.update_idletasks()

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
    run_command(command, progress_text)

    # Check if folder exists to avoid running upscale.py without a valid path
    if os.path.exists(folder_path):
        command = f"python Utils/upscale.py {folder_path}"  # Enclose folder path in quotes
        run_command(command, progress_text)

    png_folder = folder_path + "/realesrgan/"

    if os.path.exists(png_folder):
        command = f"python Utils/convertToJPG.py {png_folder}"  # Enclose folder path in quotes
        run_command(command, progress_text)

    if selected_adobe:
        command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/ \"{selected_category}\" -p a" 
        run_command(command, progress_text)

    if selected_vecteezy:
        command = f"python generateCSV/generateCSV.py {folder_path}/realesrgan/jpgs/ \"{selected_category}\" -p v" 
        run_command(command, progress_text)

    if selected_adobe:
        command = f"python Utils/sendSFTP.py {folder_path}/realesrgan/ -p a" 
        run_command(command, progress_text)

    if selected_vecteezy:
        command = f"python Utils/sendSFTP.py {folder_path}/realesrgan/jpgs/ -p v" 
        run_command(command, progress_text)

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        root.configure(bg="#2b2b2b")
        progress_text.config(bg="#2b2b2b", fg="#ffffff")

# Main window
root = tk.Tk()
root.title("Autostock Utils")
root.geometry("600x600")
root.configure(bg="#2b2b2b")
# Center the window title
root.wm_title(" " * 75 + "Autostock Utils")
root.wm_attributes("-topmost", 1)

root.iconbitmap("meulindo.ico")

# Folder selection
folder_var = tk.StringVar()
folder_label = tk.Label(root, text="Selected Folder:", bg="#2b2b2b", fg="#ffffff")
folder_label.pack(pady=5)
folder_entry = tk.Entry(root, textvariable=folder_var, width=50)
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="Select Folder", command=select_folder, bg="#004080", fg="#ffffff")
folder_button.pack(pady=5)

# Checkbox for Adobe
adobe_var = tk.BooleanVar(value=True)  # Set Adobe checkbox initially checked
adobe_checkbox = tk.Checkbutton(root, text="Adobe", variable=adobe_var, bg="#2b2b2b", fg="#ffffff", selectcolor="#004080",activebackground="#2b2b2b", activeforeground="#fff" )
adobe_checkbox.pack(pady=5)

# Checkbox for Vecteezy
vecteezy_var = tk.BooleanVar(value=True)  # Set Vecteezy checkbox initially checked
vecteezy_checkbox = tk.Checkbutton(root, text="Vecteezy", variable=vecteezy_var, bg="#2b2b2b", fg="#ffffff", selectcolor="#004080",activebackground="#2b2b2b", activeforeground="#fff")
vecteezy_checkbox.pack(pady=5)

# Category selection
category_var = tk.StringVar()
category_var.set("Select Category")
category_label = tk.Label(root, text="Select Category:", bg="#2b2b2b", fg="#ffffff")
category_label.pack(pady=5)
category_optionmenu = tk.OptionMenu(root, category_var, *categorias.values())
category_optionmenu.config(bg="#004080", fg="#ffffff")
category_optionmenu.pack(pady=5)

# Progress text
progress_text = tk.Text(root, height=15, width=60, bg="#2b2b2b", fg="#ffffff")
progress_text.pack(pady=10)

# Process button
process_button = tk.Button(root, text="Process", command=process_workflow, bg="#004080", fg="#ffffff")
process_button.pack(pady=5)

root.mainloop()
