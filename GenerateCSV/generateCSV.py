import os
import csv
import argparse
import time
from gptApi import *
from categorias import categorias
from image_describer import ImageDescriber

# Constants
PROMPTS_FOLDER_PATH = "Prompts"
PROMPTS_EXTENSION = ".txt"

def find_prompt_for_filename(filename_base):
    for prompts_file_name in os.listdir(PROMPTS_FOLDER_PATH):
        if prompts_file_name.endswith(PROMPTS_EXTENSION):
            prompts_file_path = os.path.join(PROMPTS_FOLDER_PATH, prompts_file_name)
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

def process_file(file, folder_path, language, describer):
    filename_parts = file.split("_")
    parts_that_matter = filename_parts[1:-2]
    filename_base = " ".join(parts_that_matter).strip()

    fullPrompt = find_prompt_for_filename(filename_base)
    full_file_path = os.path.join(folder_path, file)
    image_description = describer.describe_image(full_file_path, fullPrompt)

    gptTitle = createTitle(image_description, language)
    gptKeywords = getKeywords(image_description, language)
    image_category_adobe = getCategory(image_description, "a")
    image_category_dreamstime = getCategory(image_description, "d")

    gptTitle = gptTitle.strip().strip("\n").strip(",")
    gptKeywords = gptKeywords.strip(".").strip("\n")

    return {
        "filename": file,
        "gptTitle": gptTitle,
        "gptKeywords": gptKeywords,
        "image_description": image_description,
        "category_adobe": image_category_adobe,
        "category_dreamstime": image_category_dreamstime,
    }

def write_row_to_csv(writer, platform_flag, data):
    row_data = {
        'a': {
            "Filename": data["filename"],
            "Title": data["gptTitle"],
            "Keywords": data["gptKeywords"],
            "Category": data["category_adobe"], 
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
        },
        'd': {
            "Filename": data["filename"].replace('.png', '.jpg'),
            "Image Name": data["gptTitle"],
            "Description": data["image_description"],
            "Category 1": data["category_dreamstime"],
            "Category 2": "",
            "Category 3": "",
            "Keywords": data["gptKeywords"],
            "Free": 0,
            "W-EL": 1,
            "P-EL": 1,
            "SR-EL": 0,
            "SR-Pice": 0,
            "Editorial": 0,
            "MR doc Ids": "",
            "Pr Docs": "",

        },
    }[platform_flag]

    writer.writerow(row_data)

def create_writers_and_read_existing(output_folder, platform_flags, folder_name):
    csv_files = {}
    writers = {}
    existing_filenames = {}

    for platform_flag in platform_flags:
        csv_file_name = {
            'a': f"{folder_name}_adobe.csv",
            'f': f"{folder_name}_freepik.csv",
            'v': f"{folder_name}_vecteezy.csv",
            'd': f"{folder_name}_dreamstime.csv"
        }.get(platform_flag)

        if csv_file_name:
            csv_file_path = os.path.join(output_folder, csv_file_name)
            file_exists = os.path.isfile(csv_file_path)
            
            csv_files[platform_flag] = {
                "path": csv_file_path,
                "file": open(csv_file_path, "a", newline="", encoding="utf-8"),
            }

            fieldnames = {
                'a': ["Filename", "Title", "Keywords", "Category", "Releases"],
                'v': ["Filename", "Title", "Description", "Keywords", "License"],
                'f': ["Filename", "Title", "Keywords", "Prompt", "Model"],
                'd': ["Filename", "Image Name", "Description", "Category 1", "Category 2", "Category 3","Keywords","Free","W-EL","P-EL", "SR-EL","SR-Pice","Editorial","MR doc Ids","Pr Docs"]
            }[platform_flag]

            delimiter = ';' if platform_flag == 'f' else ','
            writer = csv.DictWriter(csv_files[platform_flag]["file"], fieldnames=fieldnames, delimiter=delimiter)

            if not file_exists:
                writer.writeheader()

            writers[platform_flag] = writer

            # Read existing filenames
            with open(csv_file_path, 'r', encoding='utf-8') as read_file:
                reader = csv.DictReader(read_file, delimiter=delimiter)
                existing_filenames[platform_flag] = {row['Filename'] for row in reader}

    return csv_files, writers, existing_filenames

def close_files(csv_files):
    for platform_flag, file_info in csv_files.items():
        file_info["file"].close()

def process_images(folder_path, language, describer, csv_files, writers, platform_flags, existing_filenames):
    files = get_files(folder_path)
    total_files = len(files)
    times = []

    for idx, file in enumerate(files):
        # Skip files already processed
        if any(file in existing_filenames[flag] for flag in platform_flags):
            print(f"Skipping already processed file: {file}")
            continue

        file_start_time = time.time()
        
        data = process_file(file, folder_path, language, describer)

        for platform_flag in platform_flags:
            write_row_to_csv(writers[platform_flag], platform_flag, data)

        file_end_time = time.time()
        elapsed_time = file_end_time - file_start_time
        times.append(elapsed_time)
        
        print(f"{file} processed in {elapsed_time:.2f} seconds.")

        # Calculate ETA using weighted average
        avg_time_per_file = sum(times) / len(times)
        eta_seconds = avg_time_per_file * (total_files - idx - 1)
        eta_formatted = format_eta(eta_seconds)
        print(f"Estimated time remaining: {eta_formatted} ({idx+1}/{total_files})")

    close_files(csv_files)
    print(f"Processing complete. {len(set(files))} unique files processed from the current batch.")
    return csv_files

def create_csv(folder_path, output_folder, platform_flags, language):
    folder_name = os.path.basename(os.path.normpath(folder_path))
    describer = ImageDescriber()

    csv_files, writers, existing_filenames = create_writers_and_read_existing(output_folder, platform_flags, folder_name)
    csv_files = process_images(folder_path, language, describer, csv_files, writers, platform_flags, existing_filenames)

    for platform_flag, file_info in csv_files.items():
        print(f"CSV file created successfully: {os.path.abspath(file_info['path'])}")

def main():
    parser = argparse.ArgumentParser(description='Process image folders and assign categories dynamically.')
    parser.add_argument('folder_path', type=str, help='Path to the image folder.')
    parser.add_argument('-p', '--platforms', type=str, nargs='+', choices=['a', 'f', 'v', 'd'], default=['a'],
                        help='Choose one or more platforms: -p a for Adobe, -p v for Vecteezy, -p f for Freepik')
    parser.add_argument('--language', type=str, default='pt', help='Language for titles and keywords (pt or en).')

    args = parser.parse_args()
    folder_path = args.folder_path
    output_folder = folder_path
    platform_flags = args.platforms
    language = args.language

    create_csv(folder_path, output_folder, platform_flags, language)

if __name__ == "__main__":
    main()
