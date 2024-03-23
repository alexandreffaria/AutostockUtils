import os
import sys
import csv
import argparse
from gptApi import *
from categorias import categorias

prompts_folder_path = "Prompts"
prompts_extension = ".txt"


def find_prompt_for_filename(filename_base, prompts_file_path):
    with open(prompts_file_path, "r", encoding="utf-8") as prompts_file:
        prompts = prompts_file.readlines()

    for i in range(len(filename_base), 0, -1):
        substring = filename_base[:i].strip()
        for prompt in prompts:
            if substring in prompt:
                print(f"FOUND: {substring}")
                return prompt.strip()

    return None

def create_csv(folder_path, output_folder, category, prompts_file_path):
    parent_folder_name = os.path.basename(
        os.path.normpath(os.path.join(folder_path, ".."))
    )

    # Get a list of all files in the specified folder
    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    
    csv_file_name = f"{parent_folder_name}_output.csv"
    csv_file_path = os.path.join(output_folder, csv_file_name)

    # Create a CSV file and write the header
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
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

    print(f"CSV file created successfully: {os.path.abspath(csv_file_path)}")
    print(f"Processing complete. {len(set(files))} unique files processed.")


def main():
    parser = argparse.ArgumentParser(description='Process image folders and category.')
    parser.add_argument('folder_path', type=str, help='Path to the image folder.')
    parser.add_argument('category', type=str, help='Category as a string.')

    args = parser.parse_args()
    folder_path = args.folder_path
    output_folder = folder_path  # Output folder same as image folder
    category = args.category

    category_key = next(key for key, value in categorias.items() if value == category)
    
    prompts_file_name = f"{category_key}-{category}.txt"
    prompts_file_path = os.path.join(prompts_folder_path, prompts_file_name)
    
    create_csv(folder_path, output_folder, category, prompts_file_path)


if __name__ == "__main__":
    main()
