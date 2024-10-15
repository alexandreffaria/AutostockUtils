import zipfile
import os

def unzip_files(folder: str) -> None:
    """
    Unzips all .zip files in the given folder.
    """
    for item in os.listdir(folder):
        if item.endswith('.zip'):
            file_path = os.path.join(folder, item)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(folder)
                os.remove(file_path)
                print(f"Unzipped and removed file: {file_path}")
            except zipfile.BadZipFile:
                print(f"Failed to unzip (corrupt file?): {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
