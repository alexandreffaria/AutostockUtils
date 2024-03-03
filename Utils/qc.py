import os
import sys
import imageio
import shutil
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
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

class ImageViewer(QGraphicsView):
    def __init__(self, folder_path, files):
        super().__init__()

        self.folder_path = folder_path
        self.files = files
        self.current_index = 0

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.load_image()

    def keyPressEvent(self, event):
        key = event.key()

        if key in (Qt.Key_Enter, Qt.Key_Right, Qt.Key_L, Qt.Key_H):
            self.next_image()
        elif key == Qt.Key_Left:
            self.previous_image()
        elif key == Qt.Key_X:
            self.delete_image()
        elif key == Qt.Key_Q:
            sys.exit()
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

        os.makedirs(target_folder_path, exist_ok=True)

        target_path = os.path.join(target_folder_path, file_name)

        shutil.move(source_path, target_path)

        print(f"{file_name} moved to '{target_folder}' folder.")
        del self.files[self.current_index]  # Remove the moved file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.files)
        self.load_image()

    def previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.files)
        self.load_image()

    def delete_image(self):
        if not self.files:
            return

        file_path = os.path.join(self.folder_path, self.files[self.current_index])
        os.remove(file_path)
        print(f"{self.files[self.current_index]} deleted.")
        del self.files[self.current_index]  # Remove the deleted file from the list

        if self.current_index >= len(self.files):
            self.current_index = len(self.files) - 1

        self.load_image()

    def load_image(self):
        if not self.files:
            return

        file_name = self.files[self.current_index]
        file_path = os.path.join(self.folder_path, file_name)

        # Load image using imageio with FreeImage (GPU acceleration)
        with imageio.get_reader(file_path) as reader:
            img = reader.get_data(0)  # Read the first frame

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
    app.setStyleSheet(dark_stylesheet)  # Apply dark mode stylesheet
    viewer = ImageViewer(folder_path, files)

    # Start in fullscreen mode
    viewer.showMaximized()

    viewer.show()
    sys.exit(app.exec_())
