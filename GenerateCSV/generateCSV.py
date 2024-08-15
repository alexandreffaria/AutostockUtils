import os
import csv
import argparse
from gptApi import *
from categorias import categorias
import re

# IMPLEMENT CLEAN TEXT FOR - ' é

prompts_folder_path = "Prompts"
prompts_extension = ".txt"

def clean_text(text):
    # Remove non-alphanumeric characters and spaces
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)

def find_prompt_for_filename(filename_base, prompts_file_path):
    with open(prompts_file_path, "r", encoding="utf-8") as prompts_file:
        prompts = prompts_file.readlines()

    for i in range(len(filename_base), 0, -1):
        substring = filename_base[:i].strip()
        for prompt in prompts:
            if substring in prompt:
                # print(f"FOUND: {substring}")
                return prompt.strip()

    return None

def create_csv(folder_path, output_folder, prompts_file_path, platform_flag, category_key, use_file_names, language):

    if platform_flag == 'a':
        parent_folder_name = os.path.basename(
            os.path.normpath(os.path.join(folder_path, ".."))
        )
        csv_file_name = f"{parent_folder_name}_adobe.csv"
        csv_file_path = os.path.join(output_folder, csv_file_name)

    if platform_flag == 'v':
        parent_folder_name = os.path.basename(
            os.path.normpath(os.path.join(folder_path, ".."))
        )
        csv_file_name = f"{parent_folder_name}_vecteezy.csv"
        csv_file_path = os.path.join(output_folder, csv_file_name)

    if platform_flag == 'f':
        parent_folder_name = os.path.basename(
            os.path.normpath(os.path.join(folder_path, ".."))
        )
        csv_file_name = f"{parent_folder_name}_freepik_output.csv"
        csv_file_path = os.path.join(output_folder, csv_file_name)
        
    # Get a list of all files in the specified folder with PNG or JPG extensions
    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg'))
    ]


    # Create a CSV file and write the header
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        if platform_flag == 'a':
            fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if platform_flag == 'v':
            fieldnames = ["Filename", "Title", "Description", "Keywords", "License"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if platform_flag == 'f':
            fieldnames = ["Filename", "Title", "Keywords", "Prompt", "Model"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        
        writer.writeheader()

        # Dictionary to store title and keywords for each unique filename
        filename_info = {}

        current_file_count = 0  # Counter for unique filenames

        for file in files:
            if "94574" in file:
                filename_parts = file.split("_")
                parts_that_matter = filename_parts[2:-2]
                filename_base = " ".join(parts_that_matter)
            else:
                filename_parts = file.split("_")
                parts_that_matter = filename_parts[1:-2]
                filename_base = " ".join(parts_that_matter)
            
            if filename_base not in filename_info:
                
                # Increment the counter for unique filenames
                current_file_count += 1
                fullPrompt = find_prompt_for_filename(
                    filename_base.strip(), prompts_file_path
                )
                if platform_flag == 'a':
                    if use_file_names:
                        gptTitle = (
                        createTitleWithoutPrompt(filename_base, language)
                    )
                    else:
                        gptTitle = (
                            createTitle(fullPrompt, language)
                        )
                if platform_flag == 'v':
                    if use_file_names:
                        gptTitle = (
                        createTitleWithoutPrompt(filename_base, language)
                    )
                    else:
                        gptTitle = (
                            createTitle(fullPrompt, language)
                        )
                if platform_flag == 'f':
                    if use_file_names:
                        gptTitle = (
                        clean_text(createTitleWithoutPrompt(filename_base, language))
                    )
                    else: 
                        gptTitle = (
                            clean_text(createTitle(fullPrompt, language))
                        )
            
                gptKeywords = getKeywords(fullPrompt, language)

                # Remove leading and trailing whitespaces
                gptTitle = gptTitle.strip().strip("\n").strip(",")
                gptKeywords = gptKeywords.strip(".").strip("\n")

                # Enclose keywords in double quotes
                if not platform_flag == 'f':
                    gptKeywords = f"{gptKeywords}"
                

                # Store title, keywords, and category for the unique filename
                if platform_flag == 'a':    
                    filename_info[filename_base] = {
                        "Title": gptTitle,
                        "Keywords": gptKeywords,
                        "Category": category_key,
                    }
                if platform_flag == 'v':
                    filename_info[filename_base] = {
                        "Title": gptTitle,
                        "Description": "",
                        "Keywords": gptKeywords,
                        "License": "pro",
                    }
                if platform_flag == 'f':
                    filename_info[filename_base] = {
                    "Title": gptTitle,
                    "Keywords": gptKeywords, 
                }

            # Write the information to the CSV file for the current file
            if platform_flag == 'a':
                writer.writerow(
                    {
                        "Filename": file,
                        "Title": filename_info[filename_base]["Title"],
                        "Keywords": filename_info[filename_base]["Keywords"],
                        "Category": filename_info[filename_base]["Category"],
                        "Releases": "",
                    }
                )
            
            if platform_flag == 'v':
                writer.writerow(
                    {
                        "Filename": file,
                        "Title": filename_info[filename_base]["Title"],
                        "Description": "",
                        "Keywords": filename_info[filename_base]["Keywords"],
                        "License": "pro",
                    }
                )
            
            if platform_flag == 'f':
                writer.writerow(
                    {
                        "Filename": file,
                        "Title": filename_info[filename_base]["Title"],
                        "Keywords": filename_info[filename_base]["Keywords"],
                        "Prompt": gptTitle,
                        "Model": "Midjourney 6",
                    }
                )


            print(f"{file} | written to CSV.")

    print(f"CSV file created successfully: {os.path.abspath(csv_file_path)}")
    print(f"Processing complete. {len(set(files))} unique files processed.")


def main():
    parser = argparse.ArgumentParser(description='Process image folders and category.')
    parser.add_argument('folder_path', type=str, help='Path to the image folder.')
    parser.add_argument('category', type=str, help='Category as a string.')
    parser.add_argument('-p', '--platform', choices=['a', 'f', 'v'], default='a',
                        help='Choose platform -p a for Adobe and -p v for Vecteezy or -f for Freepik')
    parser.add_argument('--no-prompt', action='store_true', 
                        help='If set, no prompt will be shown.')
    parser.add_argument('--language', type=str, default='pt', help='Language for titles and keywords (pt or en).')


    args = parser.parse_args()
    folder_path = args.folder_path
    output_folder = folder_path  
    category = args.category
    platform_flag = args.platform
    use_file_names = args.no_prompt
    language = args.language

    category_key = next(key for key, value in categorias.items() if value == category)
    
    prompts_file_name = f"{category_key}-{category}.txt"
    prompts_file_path = os.path.join(prompts_folder_path, prompts_file_name)
    
    create_csv(folder_path, output_folder, prompts_file_path, platform_flag, category_key, use_file_names, language)


if __name__ == "__main__":
    main()
