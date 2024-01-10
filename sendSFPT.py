import os
from dotenv import load_dotenv
import paramiko
import argparse
import concurrent.futures  # Add this import
from tqdm import tqdm


def load_credentials():
    # Load environment variables from .env file
    load_dotenv()

    # Get SFTP username
    username = os.getenv("SFTP_USERNAME")

    return username


def sftp_upload_file(
    local_file_path, remote_folder, hostname, port, username, password
):
    try:
        # Create an SSH client
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)

        # Create an SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Get the file name from the local path
        local_file_name = os.path.basename(local_file_path)

        # Print the name of the file before uploading
        print("Uploading:", local_file_name)

        # Upload the file
        remote_file_path = os.path.join(remote_folder, local_file_name)
        sftp.put(local_file_path, remote_file_path)
        print("Uploaded:", local_file_name)

    except Exception as e:
        print(f"Error uploading {local_file_path}: {str(e)}")

    finally:
        # Close the connections
        sftp.close()
        transport.close()


def sftp_upload_folder(
    local_folder, remote_folder, hostname, port, username, password, max_threads=48
):
    # Create an executor with a ThreadPool to upload files concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit the upload tasks for each file in the local folder
        futures = [
            executor.submit(
                sftp_upload_file,
                os.path.join(local_folder, local_file_name),
                remote_folder,
                hostname,
                port,
                username,
                password,
            )
            for local_file_name in os.listdir(local_folder)
        ]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Upload files to a remote server via SFTP"
    )
    parser.add_argument(
        "local_folder", help="Path to the local folder containing files to upload"
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Load SFTP username from .env file
    username = load_credentials()

    # Example usage
    remote_folder_path = "/path/to/remote/folder"
    hostname = "sftp.contributor.adobestock.com"
    port = 22

    # Prompt user for password
    password = input("Enter the password for {}: ".format(username))

    # Upload files from local folder to remote folder concurrently without progress bar
    sftp_upload_folder(
        args.local_folder, remote_folder_path, hostname, port, username, password
    )

    # Run the second script
    run_generate_csv_script(args.local_folder)
