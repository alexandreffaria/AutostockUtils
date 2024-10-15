import os
import glob
from typing import List, Set

def load_images(folder: str, processed_images: Set[str]) -> List[str]:
    supported_formats = ('*.jpg', '*.jpeg', '*.png')
    images = []
    for fmt in supported_formats:
        images.extend(glob.glob(os.path.join(folder, fmt)))
    images = [img for img in images if os.path.abspath(img) not in processed_images]
    images.sort()
    return images
