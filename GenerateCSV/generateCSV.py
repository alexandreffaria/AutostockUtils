import os
import csv
import argparse
from gptApi import *
from categorias import categorias
import re
from image_describer import ImageDescriber

# Constants
PROMPTS_FOLDER_PATH = "Prompts"
PROMPTS_EXTENSION = ".txt"

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
                return prompt.strip()

    return None

def create_csv(folder_path, output_folder, prompts_file_path, platform_flags, category_key, use_file_names, language):
    describer = ImageDescriber()

    csv_files = {}
    
    for platform_flag in platform_flags:
        if platform_flag == 'a':
            csv_file_name = f"{categorias[category_key]}_adobe.csv"
        elif platform_flag == 'f':
            csv_file_name = f"{categorias[category_key]}_freepik.csv"
        elif platform_flag == 'v':
            csv_file_name = f"{categorias[category_key]}_vecteezy.csv"
            
        csv_file_path = os.path.join(output_folder, csv_file_name)
        csv_files[platform_flag] = {
            "path": csv_file_path,
            "file": open(csv_file_path, "w", newline="", encoding="utf-8"),
        }

    writers = {}
    for platform_flag, file_info in csv_files.items():
        if platform_flag == 'a':
            fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]
        elif platform_flag == 'v':
            fieldnames = ["Filename", "Title", "Description", "Keywords", "License"]
        elif platform_flag == 'f':
            fieldnames = ["Filename", "Title", "Keywords", "Prompt", "Model"]

        delimiter = ';' if platform_flag == 'f' else ','
        writers[platform_flag] = csv.DictWriter(file_info["file"], fieldnames=fieldnames, delimiter=delimiter)
        writers[platform_flag].writeheader()

    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg'))
    ]

    for file in files:
        filename_parts = file.split("_")
        parts_that_matter = filename_parts[1:-2]
        filename_base = " ".join(parts_that_matter)

        fullPrompt = find_prompt_for_filename(filename_base.strip(), prompts_file_path)

        if use_file_names:
            gptTitle = createTitleWithoutPrompt(filename_base, language)
        else:
            gptTitle = createTitle(fullPrompt, language)

        full_file_path = os.path.join(folder_path, file)
        image_description = describer.describe_image(full_file_path)
        print(image_description)
        gptKeywords = getKeywords(image_description, language)

        gptTitle = gptTitle.strip().strip("\n").strip(",")
        gptKeywords = gptKeywords.strip(".").strip("\n")

        for platform_flag in platform_flags:
            if platform_flag != 'f':
                gptKeywords = f"{gptKeywords}"

            if platform_flag == 'a':
                writers[platform_flag].writerow(
                    {
                        "Filename": file,
                        "Title": gptTitle,
                        "Keywords": gptKeywords,
                        "Category": category_key,
                        "Releases": "",
                    }
                )

            elif platform_flag == 'v':
                writers[platform_flag].writerow(
                    {
                        "Filename": file,
                        "Title": gptTitle,
                        "Description": image_description,
                        "Keywords": gptKeywords,
                        "License": "pro",
                    }
                )

            elif platform_flag == 'f':
                jpg_file = file.replace('.png', '.jpg')
                writers[platform_flag].writerow(
                    {
                        "Filename": jpg_file,
                        "Title": gptTitle,
                        "Keywords": gptKeywords,
                        "Prompt": gptTitle,
                        "Model": "Midjourney 6",
                    }
                )

            print(f"{file} | written to {platform_flag.upper()} CSV.")

    for platform_flag, file_info in csv_files.items():
        file_info["file"].close()

    for platform_flag, file_info in csv_files.items():
        print(f"CSV file created successfully: {os.path.abspath(file_info['path'])}")

    print(f"Processing complete. {len(set(files))} unique files processed.")

def main():
    parser = argparse.ArgumentParser(description='Process image folders and category.')
    parser.add_argument('folder_path', type=str, help='Path to the image folder.')
    parser.add_argument('category', type=str, help='Category as a string.')
    parser.add_argument('-p', '--platforms', type=str, nargs='+', choices=['a', 'f', 'v'], default=['a'],
                        help='Choose one or more platforms: -p a for Adobe, -p v for Vecteezy, -p f for Freepik')
    parser.add_argument('--no-prompt', action='store_true', 
                        help='If set, no prompt will be shown.')
    parser.add_argument('--language', type=str, default='pt', help='Language for titles and keywords (pt or en).')

    args = parser.parse_args()
    folder_path = args.folder_path
    output_folder = folder_path  
    category = args.category
    platform_flags = args.platforms
    use_file_names = args.no_prompt
    language = args.language

    category_key = next(key for key, value in categorias.items() if value == category)
    
    prompts_file_name = f"{category_key}-{category}.txt"
    prompts_file_path = os.path.join(PROMPTS_FOLDER_PATH, prompts_file_name)
    
    create_csv(folder_path, output_folder, prompts_file_path, platform_flags, category_key, use_file_names, language)

if __name__ == "__main__":
    main()
