import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
)
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtCore import Qt
import concurrent.futures


class ImageViewer(QGraphicsView):
    def __init__(self, folder_path, files):
        super(ImageViewer, self).__init__()

        self.folder_path = folder_path
        self.files = files
        self.current_index = 0

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.load_image()

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

    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.files):
            self.load_image()

    def previous_image(self):
        self.current_index -= 1
        if self.current_index >= 0:
            self.load_image()

    def delete_image(self):
        file_path = os.path.join(self.folder_path, self.files[self.current_index])
        os.remove(file_path)
        print(f"{self.files[self.current_index]} deleted.")
        self.next_image()

    def load_image(self):
        file_name = self.files[self.current_index]
        file_path = os.path.join(self.folder_path, file_name)

        # Load image using QImageReader with hardware acceleration support
        image_reader = QImageReader(file_path)
        image_reader.setAutoTransform(True)
        image = QPixmap.fromImageReader(image_reader)

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

    # Load images concurrently using multiple cores
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(file_path): file_path for file_path in files}
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                future_to_file[future]
            except Exception as e:
                print(f"Error loading image: {e}")

    app = QApplication(sys.argv)
    viewer = ImageViewer(folder_path, files)
    viewer.show()
    sys.exit(app.exec_())
