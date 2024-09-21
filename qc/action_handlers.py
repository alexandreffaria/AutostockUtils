import os
import logging
from typing import List, Dict

from file_operations import move_file, copy_file, ensure_dir
from constants import ACTION_DELETE, ACTION_MOVE, SPECIAL_FOLDER, LULZ_FOLDER, TUT_FOLDER
from utils import get_parent_directory

def mark_image_for_deletion(file_name: str, current_index: int, files: List[str], actions_stack: List, record_entries: Dict[str, str]) -> int:
    """Mark an image for deletion."""
    logging.info(f"{file_name} marked for deletion.")
    actions_stack.append((ACTION_DELETE, file_name))
    record_entries[file_name] = ACTION_DELETE
    files.pop(current_index)
    return min(current_index, len(files) - 1)

def move_image_to_folder(file_name: str, current_index: int, files: List[str], actions_stack: List, record_entries: Dict[str, str], folder_path: str, target_folder: str) -> int:
    """Move an image to a specified folder."""
    source_path = os.path.join(folder_path, file_name)
    target_folder_path = os.path.join(folder_path, target_folder)
    target_path = os.path.join(target_folder_path, file_name)

    ensure_dir(target_folder_path)
    move_file(source_path, target_path)
    
    actions_stack.append((ACTION_MOVE, target_folder, file_name))
    record_entries[file_name] = target_folder
    files.pop(current_index)
    return min(current_index, len(files) - 1)

def copy_image_to_special(file_name: str, folder_path: str) -> None:
    """Copy an image to the 'Special' folder."""
    source_path = os.path.join(folder_path, file_name)
    special_folder_path = os.path.join(get_parent_directory(folder_path, 2), SPECIAL_FOLDER)
    target_path = os.path.join(special_folder_path, file_name)

    ensure_dir(special_folder_path)
    copy_file(source_path, target_path)

def move_image_to_external_folder(file_name: str, current_index: int, files: List[str], actions_stack: List, record_entries: Dict[str, str], folder_path: str, folder_name: str) -> int:
    """Move an image to an external folder (lulz or tut)."""
    source_path = os.path.join(folder_path, file_name)
    target_folder_path = os.path.join(get_parent_directory(folder_path, 2), folder_name)
    target_path = os.path.join(target_folder_path, file_name)

    ensure_dir(target_folder_path)
    move_file(source_path, target_path)
    
    actions_stack.append((ACTION_MOVE, folder_name, file_name))
    record_entries[file_name] = folder_name
    files.pop(current_index)
    return min(current_index, len(files) - 1)

def move_to_lulz(file_name: str, current_index: int, files: List[str], actions_stack: List, record_entries: Dict[str, str], folder_path: str) -> int:
    """Move an image to the 'lulz' folder."""
    return move_image_to_external_folder(file_name, current_index, files, actions_stack, record_entries, folder_path, LULZ_FOLDER)

def move_to_tut(file_name: str, current_index: int, files: List[str], actions_stack: List, record_entries: Dict[str, str], folder_path: str) -> int:
    """Move an image to the 'tut' folder."""
    return move_image_to_external_folder(file_name, current_index, files, actions_stack, record_entries, folder_path, TUT_FOLDER)