import os
import sys
import shutil

def organize_files_into_batches(folder_path, batch_size=1000):
    # Ensure the provided path is a directory
    if not os.path.isdir(folder_path):
        print(f"The provided path {folder_path} is not a valid directory.")
        return
    
    # Get all files in the directory
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Sort the files to maintain a consistent order
    files.sort()
    
    # Create subfolders and move files
    for i in range(0, len(files), batch_size):
        batch_folder_name = f"batch_{i // batch_size + 1}"
        batch_folder_path = os.path.join(folder_path, batch_folder_name)
        
        # Create the batch folder
        os.makedirs(batch_folder_path, exist_ok=True)
        
        # Move files to the batch folder
        for file in files[i:i + batch_size]:
            src = os.path.join(folder_path, file)
            dest = os.path.join(batch_folder_path, file)
            shutil.move(src, dest)
        
        print(f"Moved files {i + 1} to {min(i + batch_size, len(files))} into {batch_folder_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python organize_files.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        organize_files_into_batches(folder_path)
