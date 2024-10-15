import argparse
import os
import sys
from datetime import datetime

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from GenerateCSV.image_describer import ImageDescriber

def describe_images_in_folder(folder_path, title):
    # Instantiate the ImageDescriber
    image_describer = ImageDescriber()

    # Create the "stolen_prompts" directory if it doesn't exist
    os.makedirs("stolen_prompts", exist_ok=True)
    
    # Get the current date and format it as a string
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Path for the output file
    output_file_path = os.path.join("stolen_prompts", f"{current_date}.txt")

    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                image_path = os.path.join(folder_path, filename)
                description = image_describer.describe_image(image_path, title)
                
                output_file.write(f"Image: {filename}\nDescription: {description}\n\n")
                print(f"Processed {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Describe images in a folder using ImageDescriber.")
    parser.add_argument('folder_path', type=str, help="Path to the folder containing images")
    parser.add_argument('title', type=str, help="Title to be used for image description")
    args = parser.parse_args()

    describe_images_in_folder(args.folder_path, args.title)
