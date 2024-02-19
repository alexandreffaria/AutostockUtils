import os
from dotenv import load_dotenv
import paramiko
import argparse
import subprocess


def load_credentials():
    # Load environment variables from .env file
    load_dotenv()

    # Get SFTP username
    username = os.getenv("SFTP_USERNAME_adobe")
    password = os.getenv("SFTP_PASSWORD_adobe")

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


def run_generate_csv_script(local_folder, category):
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the generateCSVwithFileNames.py script
    generate_csv_script_path = os.path.join(
        current_script_dir, "generateCSVwithFileNames.py"
    )
    flagCategory = f"--category {category}"
    # Run the generateCSVwithFileNames.py script
    subprocess.run(["python", generate_csv_script_path, local_folder, flagCategory])


if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Upload files to a remote server via SFTP"
    )
    parser.add_argument(
        "local_folder", help="Path to the local folder containing files to upload"
    )
    parser.add_argument("--category", help="Category to generate csv later.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Load SFTP username from .env file
    username, password = load_credentials()

    # Example usage
    remote_folder_path = "/"
    hostname = "sftp.contributor.adobestock.com"
    port = 22

    # Upload files from local folder to remote folder
    sftp_upload_folder(
        args.local_folder, remote_folder_path, hostname, port, username, password
    )

    # Run the second script
    run_generate_csv_script(args.category)
