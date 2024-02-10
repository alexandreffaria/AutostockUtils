import os
import sys
import imageio
import shutil
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageViewer(QGraphicsView):
    def __init__(self, folder_path, files):
        super(ImageViewer, self).__init__()

        self.folder_path = folder_path
        self.files = files
        self.current_index = 0
        self.preload_count = 50  # Number of images to preload

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.preloaded_images = {}  # Dictionary to store preloaded images

        self.load_image()
        self.preload_images()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Enter:
            self.next_image()
        elif key == Qt.Key_X:
            self.delete_image()
        elif key == Qt.Key_Q:
            sys.exit()
        elif key == Qt.Key_Right or key == Qt.Key_L or key == Qt.Key_H:
            self.next_image()
        elif key == Qt.Key_Left or key == Qt.Key_H:
            self.previous_image()
        elif key == Qt.Key_W:
            self.move_image_to_folder("watermark")
        elif key == Qt.Key_B:
            self.move_image_to_folder("letterbox")

    def move_image_to_folder(self, target_folder):
        if not self.files:
            return

        file_name = self.files[self.current_index]
        source_path = os.path.join(self.folder_path, file_name)
        target_folder_path = os.path.join(self.folder_path, target_folder)

        # Create the target folder if it doesn't exist
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)

        target_path = os.path.join(target_folder_path, file_name)

        shutil.move(source_path, target_path)

        print(f"{file_name} moved to '{target_folder}' folder.")
        del self.files[self.current_index]  # Remove the moved file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()
        self.preload_images()

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.files):
            self.load_image()
            self.preload_images()

    def previous_image(self):
        self.current_index -= 1
        if self.current_index >= 0:
            self.load_image()

    def delete_image(self):
        file_path = os.path.join(self.folder_path, self.files[self.current_index])
        os.remove(file_path)
        print(f"{self.files[self.current_index]} deleted.")
        del self.files[self.current_index]  # Remove the deleted file from the list
        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1
        self.load_image()
        self.preload_images()

    def load_image(self):
        if not self.files:
            return

        file_name = self.files[self.current_index]
        file_path = os.path.join(self.folder_path, file_name)

        # Check if the image is already preloaded
        if file_name in self.preloaded_images:
            img = self.preloaded_images[file_name]
        else:
            # Load image using imageio with FreeImage (GPU acceleration)
            with imageio.get_reader(file_path) as reader:
                img = reader.get_data(0)  # Read the first frame

            # Save the image to the preload cache
            self.preloaded_images[file_name] = img

        height, width, channels = img.shape

        # Convert the image to a single QPixmap for display
        image = QPixmap.fromImage(
            QImage(img.data, width, height, width * channels, QImage.Format_RGB888)
        )

        # Set window title with current file index
        self.setWindowTitle(f"{file_name} - {self.current_index + 1}/{len(self.files)}")
        # Get the size of the viewport
        view_size = self.viewport().size()

        # Scale the image to fit the viewport
        scaled_image = image.scaled(
            view_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        item = QGraphicsPixmapItem(scaled_image)
        self.scene.clear()
        self.scene.addItem(item)

    def preload_images(self):
        # Preload the next 50 images into memory
        for i in range(
            self.current_index + 1,
            min(len(self.files), self.current_index + 1 + self.preload_count),
        ):
            file_name = self.files[i]
            file_path = os.path.join(self.folder_path, file_name)

            if file_name not in self.preloaded_images:
                with imageio.get_reader(file_path) as reader:
                    img = reader.get_data(0)
                self.preloaded_images[file_name] = img


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"The specified folder '{folder_path}' does not exist.")
        sys.exit(1)

    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    app = QApplication(sys.argv)
    viewer = ImageViewer(folder_path, files)

    # Start in fullscreen mode
    viewer.showMaximized()

    viewer.show()
    sys.exit(app.exec_())
