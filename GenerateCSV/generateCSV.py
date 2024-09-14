import os
import csv
import argparse
import re
import time
from gptApi import *
from categorias import categorias
from image_describer import ImageDescriber

# Constants
PROMPTS_FOLDER_PATH = "Prompts"
PROMPTS_EXTENSION = ".txt"

def clean_text(text):
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

def format_eta(seconds):
    hrs, remainder = divmod(seconds, 3600)
    mins, _ = divmod(remainder, 60)
    return f"{int(hrs)} hrs {int(mins)} min"

def get_files(folder_path, extensions=('.png', '.jpg')):
    return [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(extensions)
    ]

def process_file(file, folder_path, prompts_file_path, use_file_names, language, describer):
    filename_parts = file.split("_")
    parts_that_matter = filename_parts[1:-2]
    filename_base = " ".join(parts_that_matter).strip()

    fullPrompt = find_prompt_for_filename(filename_base, prompts_file_path)
    full_file_path = os.path.join(folder_path, file)
    image_description = describer.describe_image(full_file_path, fullPrompt)

    if use_file_names:
        gptTitle = createTitleWithoutPrompt(filename_base, language)
    else:
        gptTitle = createTitle(image_description, language)

    
    gptKeywords = getKeywords(image_description, language)

    gptTitle = gptTitle.strip().strip("\n").strip(",")
    gptKeywords = gptKeywords.strip(".").strip("\n")

    return {
        "filename": file,
        "gptTitle": gptTitle,
        "gptKeywords": gptKeywords,
        "image_description": image_description,
    }

def write_row_to_csv(writer, platform_flag, data, category_key):
    row_data = {
        'a': {
            "Filename": data["filename"],
            "Title": data["gptTitle"],
            "Keywords": data["gptKeywords"],
            "Category": category_key,
            "Releases": "",
        },
        'v': {
            "Filename": data["filename"],
            "Title": data["gptTitle"],
            "Description": data["image_description"],
            "Keywords": data["gptKeywords"],
            "License": "pro",
        },
        'f': {
            "Filename": data["filename"].replace('.png', '.jpg'),
            "Title": data["gptTitle"],
            "Keywords": data["gptKeywords"],
            "Prompt": data["gptTitle"],
            "Model": "Midjourney 6",
        }
    }[platform_flag]

    writer.writerow(row_data)

def create_writers(output_folder, platform_flags, category_key):
    csv_files = {}
    writers = {}

    for platform_flag in platform_flags:
        if (csv_file_name := {
            'a': f"{categorias[category_key]}_adobe.csv",
            'f': f"{categorias[category_key]}_freepik.csv",
            'v': f"{categorias[category_key]}_vecteezy.csv"
        }.get(platform_flag)):
            csv_file_path = os.path.join(output_folder, csv_file_name)
            csv_files[platform_flag] = {
                "path": csv_file_path,
                "file": open(csv_file_path, "w", newline="", encoding="utf-8"),
            }

            fieldnames = {
                'a': ["Filename", "Title", "Keywords", "Category", "Releases"],
                'v': ["Filename", "Title", "Description", "Keywords", "License"],
                'f': ["Filename", "Title", "Keywords", "Prompt", "Model"]
            }[platform_flag]

            delimiter = ';' if platform_flag == 'f' else ','
            writer = csv.DictWriter(csv_files[platform_flag]["file"], fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writers[platform_flag] = writer

    return csv_files, writers

def close_files(csv_files):
    for platform_flag, file_info in csv_files.items():
        file_info["file"].close()

def process_images(folder_path, prompts_file_path, use_file_names, language, describer, csv_files, writers, platform_flags, category_key):
    files = get_files(folder_path)
    total_files = len(files)
    start_time = time.time()

    for idx, file in enumerate(files):
        file_start_time = time.time()
        
        data = process_file(file, folder_path, prompts_file_path, use_file_names, language, describer)

        for platform_flag in platform_flags:
            write_row_to_csv(writers[platform_flag], platform_flag, data, category_key)

        file_end_time = time.time()
        elapsed_time = file_end_time - file_start_time
        print(f"{file} processed in {elapsed_time:.2f} seconds.")

        # Calculate ETA
        elapsed_total_time = file_end_time - start_time
        avg_time_per_file = elapsed_total_time / (idx + 1)
        eta_seconds = avg_time_per_file * (total_files - idx - 1)
        eta_formatted = format_eta(eta_seconds)
        print(f"Estimated time remaining: {eta_formatted} ({idx+1}/{total_files})")

    close_files(csv_files)
    print(f"Processing complete. {len(set(files))} unique files processed.")
    return csv_files

def create_csv(folder_path, output_folder, prompts_file_path, platform_flags, category_key, use_file_names, language):
    describer = ImageDescriber()

    csv_files, writers = create_writers(output_folder, platform_flags, category_key)
    csv_files = process_images(folder_path, prompts_file_path, use_file_names, language, describer, csv_files, writers, platform_flags, category_key)

    for platform_flag, file_info in csv_files.items():
        print(f"CSV file created successfully: {os.path.abspath(file_info['path'])}")

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
