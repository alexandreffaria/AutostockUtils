import os
from PIL import Image
import sys
import logging
import time
import multiprocessing
from functools import partial
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_image(file, input_folder, temp_folder):
    """
    Convert a single image to JPEG format and save to temporary folder.

    Args:
        file (str): The filename of the image to convert.
        input_folder (str): The path to the input folder.
        temp_folder (str): The path to the temporary folder.
    """
    base_filename = os.path.splitext(file)[0]
    temp_output_path = os.path.join(temp_folder, f"{base_filename}.jpg")

    # Skip if the file has already been converted
    if os.path.exists(temp_output_path):
        logging.info(f"Skipping {file} as it is already converted in temp.")
        return None

    try:
        start_time = time.time()
        image_path = os.path.join(input_folder, file)
        image = Image.open(image_path)

        # Convert and save as JPEG to temp folder
        image.convert("RGB").save(temp_output_path, "JPEG")
        end_time = time.time()
        conversion_time = end_time - start_time

        logging.info(f"Converted {file[-5:]} in {conversion_time:.2f}s")
        return conversion_time
    except Exception as e:
        logging.error(f"Error converting {file}: {e}")
        return None

def move_files(temp_folder, output_folder):
    """
    Move files from the temporary folder to the output folder.

    Args:
        temp_folder (str): The path to the temporary folder.
        output_folder (str): The path to the output folder.
    """
    try:
        files = [
            f for f in os.listdir(temp_folder)
            if os.path.isfile(os.path.join(temp_folder, f))
        ]

        for file in files:
            src_path = os.path.join(temp_folder, file)
            dest_path = os.path.join(output_folder, file)
            shutil.move(src_path, dest_path)
            logging.info(f"Moved {file} to {output_folder}")

    except Exception as e:
        logging.error(f"Error moving files: {e}")

def convert_images(input_folder: str) -> None:
    """
    Convert all images in the input folder to JPEG format using multiprocessing,
    writing to a temporary folder and then moving the files to the output folder.

    Args:
        input_folder (str): The path to the input folder containing images to convert.
    """
    try:
        # Create a folder to store the converted images
        output_folder = os.path.join(input_folder, "jpgs")
        os.makedirs(output_folder, exist_ok=True)

        # Create a unique temporary directory on the fastest drive
        temp_subfolder = tempfile.mkdtemp(prefix='image_conversion_', dir=tempfile.gettempdir())

        # Get a list of all files in the input folder
        files = [
            f for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f))
        ]

        total_files = len(files)
        num_processors = multiprocessing.cpu_count()
        logging.info(f"Starting conversion of {total_files} files using {num_processors} processors...")

        # Use multiprocessing to convert images in parallel
        pool = multiprocessing.Pool(processes=num_processors)
        func = partial(convert_image, input_folder=input_folder, temp_folder=temp_subfolder)
        conversion_times = pool.map(func, files)
        pool.close()
        pool.join()

        # Move files from temp folder to output folder
        move_files(temp_subfolder, output_folder)

        # Clean up temp subfolder
        try:
            os.rmdir(temp_subfolder)
            logging.info(f"Temporary folder {temp_subfolder} removed.")
        except OSError:
            logging.warning(f"Temporary folder {temp_subfolder} not empty, not removed.")

        # Calculate statistics
        conversion_times = [t for t in conversion_times if t is not None]
        converted_count = len(conversion_times)
        total_time = sum(conversion_times)
        avg_time_per_image = total_time / converted_count if converted_count else 0

        logging.info(f"Conversion completed. {converted_count}/{total_files} files converted.")
        logging.info(f"Total time: {total_time:.2f}s, Average time per image: {avg_time_per_image:.2f}s")

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
