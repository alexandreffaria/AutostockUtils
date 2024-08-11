import os
import sys
from PIL import Image

def get_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height

def organize_images_by_aspect_ratio(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return
    
    # Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image
        try:
            width, height = get_aspect_ratio(file_path)
        except IOError:
            print(f"Skipping non-image file: {filename}")
            continue
        
        # Calculate the aspect ratio
        aspect_ratio = f"{width}x{height}"
        
        # Create a directory for this aspect ratio if it doesn't exist
        aspect_ratio_folder = os.path.join(folder_path, aspect_ratio)
        if not os.path.exists(aspect_ratio_folder):
            os.makedirs(aspect_ratio_folder)
        
        # Move the image into the corresponding folder
        new_file_path = os.path.join(aspect_ratio_folder, filename)
        os.rename(file_path, new_file_path)
        print(f"Moved {filename} to {aspect_ratio_folder}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python organize_images.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    organize_images_by_aspect_ratio(folder_path)
