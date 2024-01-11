import os
import shutil
import sys

def create_subfolders(target_folder):
    # Create target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Get a list of all files in the target folder
    all_files = os.listdir(target_folder)

    # Sort files to ensure consistent order
    all_files.sort()

    # Create subfolders inside the target folder and move files
    subfolder_count = (len(all_files) // 100) + 1
    for i in range(subfolder_count):
        # Create subfolder inside the target folder
        subfolder_name = os.path.join(target_folder, f"{(i * 100) + 1}-{(i + 1) * 100}")
        os.makedirs(subfolder_name)

        # Determine range of files to move
        start_index = i * 100
        end_index = min((i + 1) * 100, len(all_files))

        # Move files to subfolder
        for file_name in all_files[start_index:end_index]:
            source_path = os.path.join(target_folder, file_name)
            target_path = os.path.join(subfolder_name, file_name)
            shutil.move(source_path, target_path)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py target_folder")
        sys.exit(1)

    # Get target folder from command line arguments
    target_folder = sys.argv[1]

    # Call the function to create subfolders and move files
    create_subfolders(target_folder)

    print("Files moved successfully.")
