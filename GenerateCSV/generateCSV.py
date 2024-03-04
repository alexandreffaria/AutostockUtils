import os
import sys
import csv
import tkinter as tk
from tkinter import filedialog
from gptApi import *
from categorias import categorias

prompts_folder_path = "Prompts"
prompts_extension = ".txt"


def getFolder():
    root = tk.Tk()
    root.withdraw()
    folderPath = filedialog.askdirectory(initialdir="/mnt/a/Projetos/Autostock/")
    return folderPath


def get_prompts_file_name(category):
    category_name = categorias[category]
    return f"{category}-{category_name}.txt"


def find_prompt_for_filename(filename_base, prompts_file_path):
    with open(prompts_file_path, "r") as prompts_file:
        prompts = prompts_file.readlines()
    for prompt in prompts:
        if filename_base in prompt:
            print(f"FOUND: {filename_base}")
            return prompt.strip()
    return None


def create_csv(folder_path, category, prompts_file_path):
    parent_folder_name = os.path.basename(
        os.path.normpath(os.path.join(folder_path, ".."))
    )

    # Get a list of all files in the specified folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    csv_file_name = f"{parent_folder_name}_output.csv"

    # Create a CSV file and write the header
    with open(csv_file_name, "w", newline="") as csvfile:
        fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Dictionary to store title and keywords for each unique filename
        filename_info = {}

        current_file_count = 0  # Counter for unique filenames

        for file in files:
            # Process each unique filename
            filename_base = (
                file[8:63].rsplit("_", 1)[0].replace("_", " ")
                if "_" in file[63:]
                else file[63:]
            )

            if filename_base not in filename_info:
                # Increment the counter for unique filenames
                current_file_count += 1
                fullPrompt = find_prompt_for_filename(
                    filename_base.strip(), prompts_file_path
                )
                # Prompt for title, keywords, and category for each unique filename

                gptTitle = (
                    createTitle(fullPrompt, "pt")
                    .replace("_", "")
                    .replace(".", "")
                    .replace(":", "")
                    .replace(",", "")
                    .replace("-", "")
                )
                gptTitle = (
                    gptTitle.replace(",", "")
                    .replace(".", "")
                    .replace("'", "")
                    .replace("-", "")
                )

                gptKeywords = getKeywords(gptTitle, "pt")

                # Remove leading and trailing whitespaces
                gptTitle = gptTitle.strip()
                gptTitle = gptTitle.strip("\n")
                gptTitle = gptTitle.strip(",")
                gptKeywords = gptKeywords.strip(".")
                gptKeywords = gptKeywords.strip("\n")

                # Enclose keywords in double quotes
                gptKeywords = f"{gptKeywords}"

                # Store title, keywords, and category for the unique filename
                filename_info[filename_base] = {
                    "Title": gptTitle,
                    "Keywords": gptKeywords,
                    "Category": category,
                }

            # Write the information to the CSV file for the current file
            writer.writerow(
                {
                    "Filename": file,
                    "Title": filename_info[filename_base]["Title"],
                    "Keywords": filename_info[filename_base]["Keywords"],
                    "Category": filename_info[filename_base]["Category"],
                    "Releases": "",
                }
            )

            print(f"{file} | written to CSV.")

    print(f"CSV file created successfully: {os.path.abspath(csv_file_name)}")
    print(f"Processing complete. {len(set(files))} unique files processed.")


def main():
    root = tk.Tk()
    root.title("Select Category and Folder")

    def process():
        selected_category = category_var.get()
        category_key = selected_category.split("-")[
            0
        ]  # Extracting the category key (number)
        category = int(category_key)
        folder_path = folder_var.get()
        prompts_file_name = get_prompts_file_name(category)
        prompts_file_path = os.path.join(prompts_folder_path, prompts_file_name)
        create_csv(folder_path, category, prompts_file_path)

    try:
        # Category Selection
        category_label = tk.Label(root, text="Select a Category:")
        category_label.grid(row=0, column=0, padx=10, pady=5)
        category_var = tk.StringVar(root)
        category_options = [f"{key}-{value}" for key, value in categorias.items()]
        category_dropdown = tk.OptionMenu(root, category_var, *category_options)
        category_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Folder Selection
        folder_label = tk.Label(root, text="Select Folder:")
        folder_label.grid(row=1, column=0, padx=10, pady=5)
        folder_var = tk.StringVar(root)
        folder_entry = tk.Entry(root, textvariable=folder_var, state="disabled")
        folder_entry.grid(row=1, column=1, padx=10, pady=5)
        folder_button = tk.Button(
            root, text="Browse", command=lambda: folder_var.set(getFolder())
        )
        folder_button.grid(row=1, column=2, padx=10, pady=5)

        # Process Button
        process_button = tk.Button(root, text="Process", command=process)
        process_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        root.mainloop()
        sys.exit()
    except KeyboardInterrupt:
        root.destroy()  # Explicitly destroy the Tkinter root window


if __name__ == "__main__":
    main()
