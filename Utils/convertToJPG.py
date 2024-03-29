import os
from PIL import Image
import sys

def convert_images(input_folder):
    # Create a folder to store the converted images
    output_folder = os.path.join(input_folder, "jpgs")
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of all files in the input folder
    files = [
        f
        for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
    ]

    # Convert each image to JPEG format
    for file in files:
        try:
            image_path = os.path.join(input_folder, file)
            image = Image.open(image_path)

            # Convert and save as JPEG
            output_path = os.path.join(
                output_folder, f"{os.path.splitext(file)[0]}.jpg"
            )
            image.convert("RGB").save(output_path, "JPEG")

        except Exception as e:
            pass  # Do nothing on error

    # Optionally, you can print a message after conversion completed
    # print("Conversion completed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convertToJPG.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]

    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' not found.")
        sys.exit(1)
    convert_images(input_folder)
