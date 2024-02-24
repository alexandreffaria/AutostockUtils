import os
import sys


def count_files(folder):
    file_count = 0
    for _, _, files in os.walk(folder):
        file_count += len(files)
    return file_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_files.py <folder>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("Error: The specified path is not a folder.")
        sys.exit(1)

    total_files = count_files(folder_path)
    print(f"Total files in {folder_path}: {total_files}")
