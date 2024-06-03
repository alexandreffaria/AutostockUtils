import os
import shutil

def move_png_images(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.png'):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, file)

                if os.path.exists(destination_file):
                    if os.path.getsize(source_file) < os.path.getsize(destination_file):
                        shutil.move(source_file, destination_file)
                        print(f"Moved and replaced {destination_file} with a smaller file.")
                    else:
                        print(f"Skipped {source_file} as a smaller or same size file already exists.")
                else:
                    shutil.move(source_file, destination_file)
                    print(f"Moved {source_file} to {destination_file}.")

# Example usage
source_folder = 'A:\Projetos\Autostock\Freepik'
destination_folder = 'A:\Projetos\Autostock\Freepik\pngs'
move_png_images(source_folder, destination_folder)
