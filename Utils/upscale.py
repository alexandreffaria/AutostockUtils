import os
import sys
import subprocess

def process_image(folder_path, filename):
    input_image = os.path.join(folder_path, filename)
    output_image = os.path.join(folder_path, "realesrgan", filename)
    command = [
        "realesrgan_win/realesrgan-ncnn-vulkan.exe",
        "-i", input_image,
        "-o", output_image,
        "-n", "realesrgan-x4plus"
    ]
    subprocess.run(command, check=True)

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

    os.makedirs(os.path.join(folder_path, "realesrgan"), exist_ok=True)

    for filename in png_files:
        try:
            process_image(folder_path, filename)
            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
