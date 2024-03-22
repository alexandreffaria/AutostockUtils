import tkinter as tk
from tkinter import ttk
import subprocess

def invoke_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {script_path}: {e}")


root = tk.Tk()
root.title("Autostock Utils")
root.geometry("500x500")
style = ttk.Style(root)

# Check if the 'alt' theme (a decent candidate for dark mode) is available
if 'alt' in style.theme_names():
    style.theme_use('alt')
else:
    # If 'alt' theme is not available, set the background of widgets manually
    style.configure('.', background='black')
    style.configure('TButton', background='gray20', foreground='white')
    style.configure('TCheckbutton', background='gray20', foreground='white')

# Update the root window's background color if needed
root.configure(bg='gray20')

# Utils/qc.py invocation
btn_qc = ttk.Button(root, text="Controle de qualidade", command=lambda: invoke_script('Utils/qc.py'))
btn_qc.pack(pady=5)

# Upscale realesrgan invocation
btn_upscale = ttk.Button(root, text="Upscale imagem", command=lambda: invoke_script('Utils/upscale.py'))
btn_upscale.pack(pady=5)

# SFTP Sending
btn_send_sftp = ttk.Button(root, text="Enviar imagens", command=lambda: invoke_script('Utils/sendSFTP.py'))
btn_send_sftp.pack(pady=5)

# Option selection for SFTP
option_adobe = tk.BooleanVar()
chk_adobe = tk.Checkbutton(root, text="Adobe", var=option_adobe)
chk_adobe.pack()

option_vecteezy = tk.BooleanVar()
chk_vecteezy = tk.Checkbutton(root, text="Vecteezy", var=option_vecteezy)
chk_vecteezy.pack()

# CSV Generation
btn_generate_csv = ttk.Button(root, text="Generate CSV", command=lambda: invoke_script('generateCSV.py'))
btn_generate_csv.pack(pady=5)


root.mainloop()