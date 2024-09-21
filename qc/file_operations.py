import os
import shutil
import zipfile
import logging
from typing import List, Tuple

from constants import IMAGE_EXTENSIONS

def get_zip_files(folder_path: str) -> List[str]:
    """Get a list of .zip files in the folder."""
    return [item for item in os.listdir(folder_path) if item.lower().endswith('.zip')]

def unzip_file(file_path: str, extract_to: str) -> None:
    """Unzip a single zip file."""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def remove_file(file_path: str) -> None:
    """Remove a file."""
    os.remove(file_path)

def unzip_files(folder_path: str) -> None:
    """Unzip all .zip files in the specified folder."""
    zip_files = get_zip_files(folder_path)

    for item in zip_files:
        file_path = os.path.join(folder_path, item)
        try:
            unzip_file(file_path, folder_path)
            logging.info(f"Unzipped {item}")
            remove_file(file_path)
            logging.info(f"Removed {item}")
        except Exception as e:
            logging.error(f"Error processing file {item}: {e}")

def get_image_files(folder_path: str, extensions: Tuple[str, ...] = IMAGE_EXTENSIONS) -> List[str]:
    """Get a list of image files in the folder."""
    return [
        f for f in sorted(os.listdir(folder_path))
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(extensions)
    ]

def move_file(source_path: str, target_path: str) -> None:
    """Move a file from source path to target path."""
    try:
        shutil.move(source_path, target_path)
        logging.info(f"Moved {os.path.basename(source_path)} to {os.path.dirname(target_path)}")
    except Exception as e:
        logging.error(f"Error moving file {source_path}: {e}")

def copy_file(source_path: str, target_path: str) -> None:
    """Copy a file from source path to target path."""
    try:
        shutil.copy2(source_path, target_path)
        logging.info(f"Copied {os.path.basename(source_path)} to {os.path.dirname(target_path)}")
    except Exception as e:
        logging.error(f"Error copying file {source_path}: {e}")

def ensure_dir(directory: str) -> None:
    """Ensure that a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)