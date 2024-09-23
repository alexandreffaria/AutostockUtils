import json
import os
from typing import Set, Dict

DATA_FILE = 'processed_images.json'

def get_data_file_path(folder: str) -> str:
    return os.path.join(folder, 'processed_images.json')


def load_processed_images(folder: str) -> Dict[str, Set[str]]:
    data_file = get_data_file_path(folder)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return {
                'deleted': set(os.path.abspath(p) for p in data.get('deleted', [])),
                'letterbox': set(os.path.abspath(p) for p in data.get('letterbox', [])),
                'current_index': data.get('current_index', 0)
            }
    else:
        return {'deleted': set(), 'letterbox': set(), 'current_index': 0}

def save_processed_images(
    folder: str,
    deleted: Set[str],
    letterbox: Set[str],
    current_index: int
) -> None:
    data = {
        'deleted': [os.path.abspath(p) for p in deleted],
        'letterbox': [os.path.abspath(p) for p in letterbox],
        'current_index': current_index
    }
    data_file = get_data_file_path(folder)
    with open(data_file, 'w') as f:
        json.dump(data, f)