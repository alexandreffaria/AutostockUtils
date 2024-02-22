import os
from dotenv import load_dotenv
import paramiko
import argparse


def load_credentials(platform):
    # Load environment variables from .env file
    load_dotenv()

    # Get SFTP username and password based on platform
    if platform == 'a':  # Adobe
        username = os.getenv("SFTP_USERNAME_adobe")
        password = os.getenv("SFTP_PASSWORD_adobe")
    elif platform == 'v':  # Vecteezy
        username = os.getenv("SFTP_USERNAME_vecteezy")
        password = os.getenv("SFTP_PASSWORD_vecteezy")
    else:
        raise ValueError("Invalid platform. Use 'a' for Adobe or 'v' for Vecteezy.")

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
        remote_file_path = os.path.join(remote_folder, local_file_name)

        # Upload each file
        sftp.put(local_file_path, remote_file_path)
        print("Uploaded:", local_file_name)

    # Close the connections
    sftp.close()
    transport.close()



if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Upload files to a remote server via SFTP"
    )

    parser.add_argument("-p", "--platform", help="Platform to connect (a for Adobe, v for Vecteezy)")
    parser.add_argument("local_folder", help="Path to the local folder containing files to upload")

    # Parse command-line arguments
    args = parser.parse_args()

    # Load SFTP username from .env file
    username, password = load_credentials(args.platform)

    # Example usage
    remote_folder_path = "/"
    if args.platform == 'a':
        hostname = "sftp.contributor.adobestock.com"
    elif args.platform == 'v':
        hostname = "content-ftp.eezy.com"
    port = 22

    # Upload files from local folder to remote folder
    sftp_upload_folder(
        args.local_folder, remote_folder_path, hostname, port, username, password
    )

   