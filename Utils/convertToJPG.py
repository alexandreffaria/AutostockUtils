import os
from PIL import Image
from tqdm import tqdm
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

# Dark mode stylesheet
dark_stylesheet = """
    QGraphicsView {
        background-color: #2b2b2b;
        color: #f0f0f0;
    }
"""

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

    # Convert each image to JPEG format with a progress bar
    for file in tqdm(files, desc="Converting images", unit="image"):
        try:
            image_path = os.path.join(input_folder, file)
            image = Image.open(image_path)

            # Convert and save as JPEG
            output_path = os.path.join(
                output_folder, f"{os.path.splitext(file)[0]}.jpg"
            )
            image.convert("RGB").save(output_path, "JPEG")

        except Exception as e:
            print(f"Error processing {file}: {str(e)}")

    print("Conversion completed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_stylesheet)  # Apply dark mode stylesheet
    folder_path = QFileDialog.getExistingDirectory(None, "Select the image folder", "/mnt/a")

    if not os.path.exists(folder_path):
        print(f"Error: Input folder '{folder_path}' not found.")
        sys.exit(1)

    convert_images(folder_path)
