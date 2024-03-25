import os
import shutil
import argparse
from PIL import Image

def detect_solid_color_bars(image_path, offset=5):
    image = Image.open(image_path)

    # Define the top, bottom, left, and right regions to check
    width, height = image.size
    top_region = image.crop((0, 0, width, offset))
    bottom_region = image.crop((0, height - offset, width, height))
    left_region = image.crop((0, 0, offset, height))
    right_region = image.crop((width - offset, 0, width, height))

    # Check if any of the regions are predominantly of uniform color
    if is_uniform_color(top_region) or is_uniform_color(bottom_region) \
            or is_uniform_color(left_region) or is_uniform_color(right_region):
        return True
    else:
        return False

def is_uniform_color(region, threshold=100):
    # Convert the region to RGB mode
    rgb_region = region.convert("RGB")

    # Get the color of the first pixel
    base_color = rgb_region.getpixel((0, 0))

    # Check if all pixels have the same color
    for x in range(region.width):
        for y in range(region.height):
            if sum(abs(rgb_region.getpixel((x, y))[i] - base_color[i]) for i in range(3)) > threshold:
                return False
    return True

def main(folder_path):
    # Create the output folder
    output_folder = os.path.join(folder_path, "found")
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each image file
    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, file)
            if detect_solid_color_bars(image_path):
                # Move the found image to the output folder
                shutil.move(image_path, os.path.join(output_folder, file))
                print(f"Found and moved {file} to {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect images with solid color bars.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing images')
    args = parser.parse_args()

    main(args.folder_path)
