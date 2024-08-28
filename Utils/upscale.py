import os
import sys
import subprocess
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s', handlers=[
    logging.StreamHandler(sys.stdout)
])

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
        start_time = time.time()
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        end_time = time.time()
        processing_time = end_time - start_time
        return processing_time
    except subprocess.CalledProcessError as e:
        logging.error(f"Error upscaling {filename}:\n{e.stderr}")
        return None

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

    upscaled_files = {f for f in os.listdir(output_folder) if f.endswith(".png")}

    start_time = time.time()  # Record start time
    files_to_process = [f for f in png_files if f not in upscaled_files]
    total_files = len(files_to_process)
    processed_files = 0
    cumulative_time = 0

    for filename in png_files:
        if filename in upscaled_files:
            print(f"Skipping {filename} as it is already upscaled.")
            continue

        try:
            elapsed_time = process_image(folder_path, filename)
            if elapsed_time is not None:
                processed_files += 1
                cumulative_time += elapsed_time
                avg_time = cumulative_time / processed_files
                remaining_files = total_files - processed_files
                eta = remaining_files * avg_time
                eta_hours = int(eta // 3600)
                eta_minutes = int((eta % 3600) // 60)
                logging.info(f"{processed_files}/{total_files} \nProcessed in {elapsed_time:.2f} seconds.\n{eta_hours} hrs {eta_minutes} min left")
        except Exception as e:
            logging.error(f"Error processing {filename}: {e}")

    end_time = time.time()  # Record end time
    total_elapsed_time = end_time - start_time  # Calculate total elapsed time
    logging.info(f"Total processing time: {total_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()