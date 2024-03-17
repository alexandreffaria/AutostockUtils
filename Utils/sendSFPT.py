import os
from dotenv import load_dotenv
import paramiko
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog


def getFolder():
    root = tk.Tk()
    root.withdraw()

    folderPath = filedialog.askdirectory(initialdir="/mnt/a/Projetos/Autostock/")

    return folderPath


def load_credentials():
    load_dotenv()
    username = os.getenv("SFTP_USERNAME_adobe")
    password = os.getenv("SFTP_PASSWORD_adobe")
    return username, password


def sftp_upload_folder(local_folder, remote_folder, hostname, port, username, password):
    # Create an SSH client
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)

    # Create an SFTP client
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Get total number of files for progress bar
    num_files = len(os.listdir(local_folder))

    # Use tqdm for progress bar
    with tqdm(total=num_files, desc="Uploading", unit="file") as pbar:
        # Iterate through all files in the local folder
        for local_file_name in os.listdir(local_folder):
            local_file_path = os.path.join(local_folder, local_file_name)
            remote_file_path = os.path.join(remote_folder, local_file_name)

            # Upload each file
            sftp.put(local_file_path, remote_file_path)
            pbar.update(1)  # Update progress bar
            pbar.set_postfix(file=local_file_name)

    # Close the connections
    sftp.close()
    transport.close()


if __name__ == "__main__":
    # Load SFTP username from .env file
    username, password = load_credentials()

    remote_folder_path = "/"
    hostname = "sftp.contributor.adobestock.com"
    port = 22

    imageFolder = getFolder()
    print(imageFolder)
    # Upload files from local folder to remote folder
    sftp_upload_folder(
        imageFolder, remote_folder_path, hostname, port, username, password
    )
