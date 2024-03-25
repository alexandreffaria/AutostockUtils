import os
import shutil
import argparse
from PIL import Image

def detect_solid_color_bars(image_path, offset=5, threshold=100):
    image = Image.open(image_path)

    # Define the top, bottom, left, and right regions to check
    width, height = image.size
    top_region = image.crop((0, 0, width, offset))
    bottom_region = image.crop((0, height - offset, width, height))
    left_region = image.crop((0, 0, offset, height))
    right_region = image.crop((width - offset, 0, width, height))

    # Check if any of the regions are predominantly of uniform color
    if is_uniform_color(top_region, threshold) or is_uniform_color(bottom_region, threshold) \
            or is_uniform_color(left_region, threshold) or is_uniform_color(right_region, threshold):
        return True, image
    else:
        return False, None

def is_uniform_color(region, threshold):
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

def create_mask(image, output_folder):
    width, height = image.size

    # Create a new blank image for the mask
    mask = Image.new("L", (width, height), color=0)

    # Get the solid color
    solid_color = get_solid_color(image)

    # Paint pixels in the mask based on solid color detection
    mask_pixels = mask.load()
    for x in range(width):
        for y in range(height):
            pixel_color = image.getpixel((x, y))
            if pixel_color == solid_color:
                mask_pixels[x, y] = 255  # Paint white
            else:
                mask_pixels[x, y] = 0    # Paint black

    # Save the mask image
    mask_path = os.path.join(output_folder, f"mask_{os.path.basename(image.filename)}")
    mask.save(mask_path)
    print(f"Mask created: {mask_path}")

def get_solid_color(image):
    width, height = image.size
    colors = {}

    # Iterate over all pixels to count occurrences of each color
    for x in range(width):
        for y in range(height):
            color = image.getpixel((x, y))
            if color in colors:
                colors[color] += 1
            else:
                colors[color] = 1

    # Find the most common color (solid color)
    solid_color = max(colors, key=colors.get)

    return solid_color

def main(folder_path):
    # Create the output folder for found images and masks
    output_folder = os.path.join(folder_path, "found")
    masks_folder = os.path.join(folder_path, "masks")
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(masks_folder, exist_ok=True)

    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each image file
    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, file)

            # Detect solid color bars in the image
            solid_color_detected, image = detect_solid_color_bars(image_path)
            if solid_color_detected:
                # Move the found image to the output folder
                shutil.move(image_path, os.path.join(output_folder, file))
                print(f"Found and moved {file} to {output_folder}")

                # Create the mask for the found image
                create_mask(image, masks_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect images with solid color bars.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing images')
    args = parser.parse_args()

    main(args.folder_path)
