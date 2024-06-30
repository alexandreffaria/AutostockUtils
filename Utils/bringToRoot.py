import os
import shutil
import sys

def move_files_to_root(directory):
    """Move all files from subdirectories to the root directory."""
    for root, dirs, files in os.walk(directory):
        if root == directory:
            # Skip the root directory itself
            continue
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(directory, file)
            print(f"Moving {src_path} to {dest_path}")
            shutil.move(src_path, dest_path)

    # Optionally remove empty directories after all files have been moved
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty directory {dir_path}")
            except OSError:
                print(f"Could not remove {dir_path} (not empty or permission denied)")

def main():
    if len(sys.argv) != 2:
        print("Usage: python bringToRoot.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    move_files_to_root(directory)

if __name__ == "__main__":
    main()
