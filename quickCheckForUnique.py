import os
import shutil
import sys


def compare_and_move(ohgod_folder, original_folder, unique_folder):
    # Get the list of files in each folder
    ohgod_files = set(os.listdir(ohgod_folder))
    original_files = set(os.listdir(original_folder))

    # Find files in 'ohgod' that do not exist in 'original'
    unique_files = ohgod_files - original_files

    # Move unique files to the 'unique' folder
    for file_name in unique_files:
        source_path = os.path.join(ohgod_folder, file_name)
        destination_path = os.path.join(unique_folder, file_name)
        shutil.move(source_path, destination_path)
        print(f"Moved '{file_name}' to 'unique' folder.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <ohgod_folder> <original_folder>")
        sys.exit(1)

    ohgod_folder = sys.argv[1]
    original_folder = sys.argv[2]
    unique_folder = os.path.join(os.path.dirname(ohgod_folder), "unique")

    # Create 'unique' folder if it doesn't exist
    if not os.path.exists(unique_folder):
        os.makedirs(unique_folder)
        print(f"Created 'unique' folder at {unique_folder}")

    compare_and_move(ohgod_folder, original_folder, unique_folder)
