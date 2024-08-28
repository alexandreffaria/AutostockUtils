import os
import sys
import subprocess
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_image(folder_path, filename):
    input_image = os.path.join(folder_path, filename)
    output_image = os.path.join(folder_path, "realesrgan", filename)
    command = [
        "realesrgan_win/realesrgan-ncnn-vulkan.exe",
        "-i", input_image,
        "-o", output_image,
        "-n", "realesrgan-x4plus"
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Output of upscaling {filename}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error upscaling {filename}:\n{e.stderr}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 upscale.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("Error: Folder path is invalid.")
        sys.exit(1)

    png_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
    if not png_files:
        print("Error: No PNG files found in the specified folder.")
        sys.exit(1)

    output_folder = os.path.join(folder_path, "realesrgan")
    os.makedirs(output_folder, exist_ok=True)

    start_time = time.time()  # Record start time

    for filename in png_files:
        output_image = os.path.join(output_folder, filename)
        if os.path.exists(output_image):
            print(f"Skipping {filename} as it is already upscaled.")
            continue

        try:
            process_image(folder_path, filename)
            print(f"Processed: {filename}")
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    logging.info(f"Total processing time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
