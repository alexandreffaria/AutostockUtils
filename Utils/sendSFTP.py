import os
import pysftp
import argparse
import ftplib
import logging
import time
from dotenv import load_dotenv
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_credentials(platform):
    load_dotenv()
    if platform == "a":  # Adobe
        username = os.getenv("SFTP_USERNAME_adobe")
        password = os.getenv("SFTP_PASSWORD_adobe")
    elif platform == "v":  # Vecteezy
        username = os.getenv("SFTP_USERNAME_vecteezy")
        password = os.getenv("SFTP_PASSWORD_vecteezy")
    elif platform == "f":  # Freepik
        username = os.getenv("SFTP_USERNAME_freepik")
        password = os.getenv("SFTP_PASSWORD_freepik")
    else:
        raise ValueError("Invalid platform. Use 'a' for Adobe, 'v' for Vecteezy, or 'f' for Freepik")
    return username, password

@contextmanager
def sftp_connection_pysftp(hostname, username, password):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disables host key checking for simplicity
    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        yield sftp

def sftp_upload_folder_pysftp(local_folder, remote_folder, hostname, username, password):
    with sftp_connection_pysftp(hostname, username, password) as sftp:
        sftp.makedirs(remote_folder)
        for local_file_name in os.listdir(local_folder):
            local_file_path = os.path.join(local_folder, local_file_name)
            if local_file_name.lower().endswith(('.png', '.jpg')) and os.path.isfile(local_file_path):
                remote_file_path = os.path.join(remote_folder, local_file_name)
                for attempt in range(3):
                    try:
                        sftp.put(local_file_path, remote_file_path)
                        logging.info(f"Uploaded: {local_file_path} to {remote_file_path}")
                        break
                    except Exception as e:
                        logging.error(f"Error uploading {local_file_path}: {e}")
                        time.sleep(2 ** attempt)
                        if attempt == 2:
                            logging.error(f"Failed to upload {local_file_path} after 3 attempts")

@contextmanager
def ftp_connection(hostname, username, password):
    ftp = ftplib.FTP(hostname)
    try:
        ftp.login(username, password)
        yield ftp
    finally:
        ftp.quit()

def ftp_upload_folder(local_folder, remote_folder, hostname, username, password):
    with ftp_connection(hostname, username, password) as ftp:
        for local_file_name in os.listdir(local_folder):
            local_file_path = os.path.join(local_folder, local_file_name)
            if local_file_name.lower().endswith(('.png', '.jpg')) and os.path.isfile(local_file_path):
                remote_file_path = os.path.join(remote_folder, local_file_name)
                for attempt in range(3):
                    try:
                        with open(local_file_path, 'rb') as file:
                            ftp.storbinary(f'STOR {remote_file_path}', file)
                            logging.info(f"Uploaded: {local_file_path} to {remote_file_path}")
                            break
                    except ftplib.all_errors as e:
                        logging.error(f"Error uploading {local_file_path}: {e}")
                        time.sleep(2 ** attempt)
                        if attempt == 2:
                            logging.error(f"Failed to upload {local_file_path} after 3 attempts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload files to a remote server via SFTP or FTP")
    parser.add_argument("-p", "--platform", required=True, help="Platform to connect (a for Adobe, v for Vecteezy, f for Freepik)")
    parser.add_argument("local_folder", help="Path to the local folder containing files to upload")

    args = parser.parse_args()
    username, password = load_credentials(args.platform)

    if args.platform == "a":
        logging.info("Sending to Adobe")
        sftp_upload_folder_pysftp(args.local_folder, "/", "sftp.contributor.adobestock.com", username, password)
    elif args.platform == "f":
        logging.info("Sending to Freepik")
        ftp_upload_folder(args.local_folder, "/", "contributor-ftp.freepik.com", username, password)
    elif args.platform == "v":
        logging.info("Sending to Vecteezy")
        sftp_upload_folder_pysftp(args.local_folder, "cm-prod-ftp-bucket/alexandreffaria61364/", "content-ftp.eezy.com", username, password)
    else:
        raise ValueError("Invalid platform. Use 'a' for Adobe, 'v' for Vecteezy, or 'f' for Freepik")
