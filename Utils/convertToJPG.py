import os
from PIL import Image
import sys
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_images(input_folder: str) -> None:
    """
    Convert all images in the input folder to JPEG format and save them in a 'jpgs' subfolder.

    Args:
        input_folder (str): The path to the input folder containing images to convert.
    """
    try:
        # Create a folder to store the converted images
        output_folder = os.path.join(input_folder, "jpgs")
        os.makedirs(output_folder, exist_ok=True)

        # Get a list of all files in the input folder
        files = [
            f for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f))
        ]

        # Check which files have already been converted
        existing_converted_files = set(
            os.path.splitext(f)[0] for f in os.listdir(output_folder)
            if os.path.isfile(os.path.join(output_folder, f))
        )

        total_files = len(files)
        converted_count = 0
        total_time = 0

        # Convert each image to JPEG format
        for index, file in enumerate(files):
            base_filename = os.path.splitext(file)[0]
            if base_filename in existing_converted_files:
                logging.info(f"Skipping {file} as it is already converted.")
                continue

            try:
                start_time = time.time()
                
                image_path = os.path.join(input_folder, file)
                image = Image.open(image_path)

                # Convert and save as JPEG
                output_path = os.path.join(
                    output_folder, f"{base_filename}.jpg"
                )
                image.convert("RGB").save(output_path, "JPEG")
                
                end_time = time.time()
                conversion_time = end_time - start_time
                total_time += conversion_time
                converted_count += 1
                avg_time_per_image = total_time / converted_count
                remaining_images = total_files - converted_count
                estimated_remaining_time = remaining_images * avg_time_per_image
                
                est_hours = int(estimated_remaining_time // 3600)
                est_minutes = int((estimated_remaining_time % 3600) // 60)

                logging.info(f"Converted {file[-5:]} in {conversion_time:.2f}s - ({index + 1}/{total_files})\nTime left: {est_hours} hrs {est_minutes} min")

            except Exception as e:
                logging.error(f"Error converting {file}: {e}")

        logging.info(f"Conversion completed. {converted_count}/{total_files} files converted.")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python convertToJPG.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]

    if not os.path.exists(input_folder):
        logging.error(f"Error: Input folder '{input_folder}' not found.")
        sys.exit(1)

    convert_images(input_folder)
