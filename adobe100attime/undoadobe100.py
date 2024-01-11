import os
import shutil
import sys

def undo_subfolder_organization(target_folder):
    # Get a list of all subfolders in the target folder
    subfolders = [f.path for f in os.scandir(target_folder) if f.is_dir()]

    # Sort subfolders to ensure consistent order
    subfolders.sort()

    # Iterate through subfolders and move files back to the target folder
    for subfolder in subfolders:
        files_in_subfolder = os.listdir(subfolder)
        for file_name in files_in_subfolder:
            source_path = os.path.join(subfolder, file_name)
            target_path = os.path.join(target_folder, file_name)
            shutil.move(source_path, target_path)

        # Remove the empty subfolder
        os.rmdir(subfolder)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py target_folder")
        sys.exit(1)

    # Get target folder from command line arguments
    target_folder = sys.argv[1]

    # Call the function to undo subfolder organization
    undo_subfolder_organization(target_folder)

    print("Files moved back successfully.")
