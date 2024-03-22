import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from subprocess import Popen, PIPE

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

    command = f"python Utils/qc.py \"{folder_path}\""  # Enclose folder path in quotes
    run_command(command, progress_text)

    # Check if folder exists to avoid running upscale.py without a valid path
    if os.path.exists(folder_path):
        command = f"python Utils/upscale.py \"{folder_path}\""  # Enclose folder path in quotes
        run_command(command, progress_text)

    png_folder = os.path.join(folder_path, "upscayl_png_realesrgan-x4plus_4x")
    if os.path.exists(png_folder):
        command = f"python convertToJPG.py \"{png_folder}\""  # Enclose folder path in quotes
        run_command(command, progress_text)

    command = f"python Utils/sendSFPT.py -v \"{folder_path}\""  # Enclose folder path in quotes
    run_command(command, progress_text)

    command = f"python Utils/sendSFPT.py -a \"{folder_path}\""  # Enclose folder path in quotes
    run_command(command, progress_text)

    command = f"python generateCSV/generateCSV.py -a \"{folder_path}\""  # Enclose folder path in quotes
    run_command(command, progress_text)

    command = f"python generateCSV/generateCSV.py -v \"{folder_path}\""  # Enclose folder path in quotes
    run_command(command, progress_text)

# Function to select a folder
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

# Folder selection
folder_var = tk.StringVar()
folder_label = tk.Label(root, text="Selected Folder:", bg="#2b2b2b", fg="#ffffff")
folder_label.pack(pady=5)
folder_entry = tk.Entry(root, textvariable=folder_var, width=50)
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="Select Folder", command=select_folder, bg="#004080", fg="#ffffff")
folder_button.pack(pady=5)

# Progress text
progress_text = tk.Text(root, height=15, width=60, bg="#2b2b2b", fg="#ffffff")
progress_text.pack(pady=10)

# Process button
process_button = tk.Button(root, text="Process", command=process_workflow, bg="#004080", fg="#ffffff")
process_button.pack(pady=5)

root.mainloop()
