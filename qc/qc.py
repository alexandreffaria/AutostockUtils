from typing import List
from cli_module import parse_arguments
from image_loader import load_images
from gui_module import ImageViewer
from key_bindings import get_key_bindings
from data_manager import load_processed_images, save_processed_images
from unzip import unzip_files
import os

def main() -> None:
    folder = parse_arguments()
    unzip_files(folder)
    processed_images = load_processed_images(folder)
    all_processed_images = processed_images['deleted'] | processed_images['letterbox']
    current_index = processed_images.get('current_index', 0)

    # Remove any previously processed images that reappear in the folder
    for image_path in all_processed_images:
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Deleted previously processed image: {image_path}")
            except Exception as e:
                print(f"Error deleting image {image_path}: {e}")

    # Load images, excluding processed ones
    images = load_images(folder, all_processed_images)
    if not images:
        print("No images to display.")
        return

    viewer = ImageViewer(images, {}, processed_images, start_index=current_index)
    key_bindings = get_key_bindings(viewer)
    viewer.key_bindings = key_bindings
    viewer.bind_keys()
    try:
        viewer.start()
    finally:
        save_processed_images(folder, viewer.deleted_images, viewer.letterbox_images, viewer.current_index)
if __name__ == "__main__":
    main()
