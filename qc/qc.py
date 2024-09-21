import os
import sys
import logging
from typing import List, Dict

# Import functions from other modules
from file_operations import unzip_files, get_image_files
from record_management import read_record_file, read_state_file
from image_viewer import ImageViewer
from utils import load_environment_variables
from constants import IMAGE_EXTENSIONS

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    setup_logging()
    load_environment_variables()

    if len(sys.argv) != 2:
        logging.error("Usage: python3 main.py /path/to/images")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        logging.error(f"The specified folder '{folder_path}' does not exist.")
        sys.exit(1)

    unzip_files(folder_path)

    record_file_path = os.path.join(folder_path, 'qc_record.txt')
    existing_records = read_record_file(record_file_path)

    all_files = get_image_files(folder_path, IMAGE_EXTENSIONS)

    # Exclude images that have already been QC'ed
    qc_images = set(existing_records.keys())
    files_to_view = [f for f in all_files if f not in qc_images]

    if not files_to_view:
        logging.info("All images have been QC'ed.")
        sys.exit(0)

    # Read last viewed image from state file
    state_file_path = os.path.join(folder_path, 'qc_state.txt')
    last_image = read_state_file(state_file_path)

    viewer = ImageViewer(folder_path, files_to_view, last_image, existing_records)
    viewer.mainloop()

if __name__ == "__main__":
    main()