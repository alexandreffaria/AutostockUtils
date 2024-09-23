import tkinter as tk
import os, shutil
from typing import Callable, Dict, Tuple, Any
from gui_module import ImageViewer, KeyBindingsType

def next_image(event: tk.Event, viewer: ImageViewer) -> None:
    viewer.next_image()

def previous_image(event: tk.Event, viewer: ImageViewer) -> None:
    viewer.previous_image()

def delete_image(event: tk.Event, viewer: ImageViewer) -> None:
    image_path = os.path.abspath(viewer.image_paths[viewer.current_index])
    trash_folder = os.path.join(os.path.dirname(image_path), '.trash')
    os.makedirs(trash_folder, exist_ok=True)
    dest_path = os.path.join(trash_folder, os.path.basename(image_path))
    
    # Move the file to the trash folder
    shutil.move(image_path, dest_path)
    viewer.deleted_images.add(image_path)
    
    # Record the action for undo
    viewer.undo_stack.append({
        'action': 'delete',
        'original_path': image_path,
        'deleted_path': dest_path,
        'index': viewer.current_index
    })
    
    # Remove the image from the list
    del viewer.image_paths[viewer.current_index]
    
    if viewer.current_index >= len(viewer.image_paths):
        viewer.current_index = 0
    
    if viewer.image_paths:
        viewer.display_image(viewer.current_index)
    else:
        viewer.root.destroy()  # Close the app if no images left

def move_to_letterbox(event: tk.Event, viewer: ImageViewer) -> None:
    image_path = os.path.abspath(viewer.image_paths[viewer.current_index])
    letterbox_folder = os.path.join(os.path.dirname(image_path), 'letterbox')
    os.makedirs(letterbox_folder, exist_ok=True)
    dest_path = os.path.join(letterbox_folder, os.path.basename(image_path))
    
    # Move the file to the letterbox folder
    shutil.move(image_path, dest_path)
    viewer.letterbox_images.add(image_path)
    
    # Record the action for undo
    viewer.undo_stack.append({
        'action': 'move',
        'original_path': image_path,
        'moved_path': dest_path,
        'index': viewer.current_index
    })
    
    # Remove the image from the list
    del viewer.image_paths[viewer.current_index]
    if viewer.current_index >= len(viewer.image_paths):
        viewer.current_index = 0
    
    if viewer.image_paths:
        viewer.display_image(viewer.current_index)
    else:
        viewer.root.destroy()

def undo_action(event: tk.Event, viewer: ImageViewer) -> None:
    if not viewer.undo_stack:
        print("Nothing to undo")
        return
    
    last_action = viewer.undo_stack.pop()
    if last_action['action'] == 'delete':
        # Move the file back from the trash to the original location
        shutil.move(last_action['deleted_path'], last_action['original_path'])
        viewer.deleted_images.remove(last_action['original_path'])
        
        # Insert the image back into image_paths
        viewer.image_paths.insert(last_action['index'], last_action['original_path'])
        viewer.current_index = last_action['index']
        viewer.display_image(viewer.current_index)
        
    elif last_action['action'] == 'move':
        # Move the file back from the letterbox folder to the original location
        shutil.move(last_action['moved_path'], last_action['original_path'])
        viewer.letterbox_images.remove(last_action['original_path'])
        
        # Insert the image back into image_paths
        viewer.image_paths.insert(last_action['index'], last_action['original_path'])
        viewer.current_index = last_action['index']
        viewer.display_image(viewer.current_index)

def get_key_bindings(viewer: ImageViewer) -> KeyBindingsType:
    return {
        ('<l>', '<Right>'): lambda event: next_image(event, viewer),
        ('<h>', '<Left>'): lambda event: previous_image(event, viewer),
        ('<d>',): lambda event: delete_image(event, viewer),
        ('<m>',): lambda event: move_to_letterbox(event, viewer),
        ('<u>',): lambda event: undo_action(event, viewer),
    }
