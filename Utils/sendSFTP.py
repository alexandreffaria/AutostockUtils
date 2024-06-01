import os
from dotenv import load_dotenv
import paramiko
import argparse
import ftplib

def load_credentials(platform):
    # Load environment variables from .env file
    load_dotenv()

    # Get SFTP username and password based on platform
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
        raise ValueError("Invalid platform. Use 'a' for Adobe or 'v' for Vecteezy or 'f' for Freepik")

    return username, password

def sftp_upload_folder(local_folder, remote_folder, hostname, port, username, password):
    # Create an SSH client
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)

    # Create an SFTP client
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Iterate through all files in the local folder
    for local_file_name in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, local_file_name)

        # Check if the file is PNG or JPG and is a file (not directory)
        if local_file_name.lower().endswith(('.png', '.jpg')) and os.path.isfile(local_file_path):
            remote_file_path = os.path.join(remote_folder, local_file_name)

            # Upload the file
            sftp.put(local_file_path, remote_file_path)

    # Close the connections
    sftp.close()
    transport.close()

def ftp_upload_folder(local_folder, remote_folder, hostname, username, password):
    # Connect to FTP server
    ftp = ftplib.FTP(hostname)
    ftp.login(username, password)

    # Iterate through all files in the local folder
    for local_file_name in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, local_file_name)

        # Check if the file is PNG or JPG and is a file (not directory)
        if local_file_name.lower().endswith(('.png', '.jpg')) and os.path.isfile(local_file_path):
            remote_file_path = os.path.join(remote_folder, local_file_name)

            # Upload the file
            with open(local_file_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_file_path}', file)

    # Close the connection
    ftp.quit()

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Upload files to a remote server via SFTP"
    )

    parser.add_argument(
        "-p", "--platform", help="Platform to connect (a for Adobe, v for Vecteezy)"
    )
    parser.add_argument(
        "local_folder", help="Path to the local folder containing files to upload"
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Load SFTP username from .env file
    username, password = load_credentials(args.platform)

    port = 22

    if args.platform == "a":
        print("Sending to Adobe")
        remote_folder_path = "/"
        hostname = "sftp.contributor.adobestock.com"
        sftp_upload_folder(
            args.local_folder, remote_folder_path, hostname, port, username, password
        )
        
    elif args.platform == "f":
        print("Sending to Freepik")
        remote_folder_path = "/"
        hostname = "contributor-ftp.freepik.com"
        ftp_upload_folder(
            args.local_folder, remote_folder_path, hostname, username, password
        )
        # port = 21

    elif args.platform == "v":
        print("Sending to Vecteezy")
        remote_folder_path = "cm-prod-ftp-bucket/alexandreffaria61364/"
        hostname = "content-ftp.eezy.com"
        sftp_upload_folder(
            args.local_folder, remote_folder_path, hostname, port, username, password
        )
    else:
        raise ValueError("Invalid platform. Use 'a' for Adobe or 'v' for Vecteezy.")
    