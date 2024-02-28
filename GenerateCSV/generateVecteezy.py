import os
import csv
import argparse
from tqdm import tqdm
from gptApi import *
from categorias import categorias
import re

prompts_folder_path = "Prompts"
prompts_extension = ".txt"


def get_prompts_file_name(category):
    category_name = categorias[category]
    return f"{category}-{category_name}.txt"


def find_prompt_for_filename(filename_base, prompts_file_path):
    with open(prompts_file_path, "r") as prompts_file:
        prompts = prompts_file.readlines()
    for prompt in prompts:
        if filename_base in prompt:
            return prompt.strip()
    return None


def clean_text(text):
    # Remove non-alphanumeric characters and spaces
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def create_csv(folder_path, category, prompts_file_path):
    parent_folder_name = os.path.basename(
        os.path.normpath(os.path.join(folder_path, "../.."))
    )

    # Get a list of all files in the specified folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    csv_file_name = f"{parent_folder_name}_vect_output.csv"

    # Create a CSV file and write the header
    with open(csv_file_name, "w", newline="") as csvfile:
        fieldnames = ["Filename", "Title", "Description", "Keywords", "License"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Dictionary to store title and keywords for each unique filename
        filename_info = {}

        current_file_count = 0  # Counter for unique filenames

        # Integrate tqdm for progress bar
        for file in tqdm(files, desc="Processing files", unit="file"):
            # Process each unique filename
            filename_base = os.path.splitext(file)[0]  # Remove file extension
            filename_base_prompt = (
                file[8:63].rsplit("_", 1)[0].replace("_", " ")
                if "_" in file[63:]
                else file[63:]
            )

            if filename_base not in filename_info:
                # Increment the counter for unique filenames
                current_file_count += 1
                fullPrompt = find_prompt_for_filename(
                    filename_base_prompt.strip(), prompts_file_path
                )

                # Prompt for title, keywords, and category for each unique filename
                gptTitle = createTitle(fullPrompt, "en")
                gptKeywords = getKeywords(fullPrompt, "en").replace("-", "")
                gptKeywords = "ai generated," + gptKeywords
                # Clean title and keywords
                gptTitle = clean_text(gptTitle)
                gptTitle = "AI generated " + gptTitle

                # Store title, keywords, and category for the unique filename
                filename_info[filename_base] = {
                    "Title": gptTitle,
                    "Description": "",  # No change in description
                    "Keywords": gptKeywords,
                }

            # Write the information to the CSV file for the current file
            writer.writerow(
                {
                    "Filename": filename_base,  # Update filename without extension
                    "Title": filename_info[filename_base]["Title"],
                    "Description": filename_info[filename_base]["Description"],
                    "Keywords": filename_info[filename_base]["Keywords"],
                    "License": "Free",
                }
            )

    print(f"CSV file created successfully: {os.path.abspath(csv_file_name)}")
    print(f"Processing complete. {len(set(files))} unique files processed.")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Create a CSV file with filenames from a specified folder."
    )
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing files."
    )
    parser.add_argument("--category", type=int, help="Category of the images.")

    # Parse the command-line arguments
    args = parser.parse_args()

    prompts_file_name = get_prompts_file_name(args.category)
    prompts_file_path = os.path.join(prompts_folder_path, prompts_file_name)

    # Call the function to create the CSV file
    create_csv(args.folder_path, args.category, prompts_file_path)
