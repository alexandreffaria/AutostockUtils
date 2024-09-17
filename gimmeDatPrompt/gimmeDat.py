import os
import sys
from datetime import datetime
from PIL import Image
import image_interrogator

def process_images_in_folder(folder_path, output_dir, mode='best'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create the output file with the current date in its name
    current_date = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f'prompts_{current_date}.txt')
    
    with open(output_file, 'w') as f:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(folder_path, filename)
                try:
                    image = Image.open(image_path)
                    prompt = image_interrogator.image_to_prompt(image, mode)
                    f.write(prompt + '\n')
                    print(f"Processed {filename}")
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gimmeDat.py <image_folder> [mode]")
        sys.exit(1)

    folder_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'best'

    if not os.path.isdir(folder_path):
        print(f"The specified path {folder_path} is not a directory.")
        sys.exit(1)
    
    # Define the 'stolen_prompts' folder
    output_dir = os.path.join(os.getcwd(), 'stolen_prompts')
    
    process_images_in_folder(folder_path, output_dir, mode)
