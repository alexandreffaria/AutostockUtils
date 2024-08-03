import os
import paramiko
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file in the parent directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Load common SFTP configuration from environment variables
SFTP_PORT = int(os.getenv('SFTP_PORT', 22))
REMOTE_PATH = os.getenv('REMOTE_PATH', '.')

# Load specific SFTP credentials for platforms
SFTP_USERNAME_ADOBE = os.getenv('SFTP_USERNAME_adobe')
SFTP_PASSWORD_ADOBE = os.getenv('SFTP_PASSWORD_adobe')
SFTP_HOST_ADOBE = os.getenv('SFTP_HOST_adobe')
SFTP_USERNAME_FREEPIK = os.getenv('SFTP_USERNAME_freepik')
SFTP_PASSWORD_FREEPIK = os.getenv('SFTP_PASSWORD_freepik')
SFTP_HOST_FREEPIK = os.getenv('SFTP_HOST_freepik')

def upload_files(local_folder: str, platform: str) -> None:
    """
    Upload files to an SFTP server based on the platform.

    Args:
        local_folder (str): The local folder containing files to upload.
        platform (str): The platform name (adobe or freepik).
    """
    if platform == "a":
        username = SFTP_USERNAME_ADOBE
        password = SFTP_PASSWORD_ADOBE
        sftp_host = SFTP_HOST_ADOBE
    elif platform == "f":
        username = SFTP_USERNAME_FREEPIK
        password = SFTP_PASSWORD_FREEPIK
        sftp_host = SFTP_HOST_FREEPIK
    else:
        logging.error(f"Unknown platform: {platform}")
        return

    try:
        # Initialize SFTP connection
        transport = paramiko.Transport((sftp_host, SFTP_PORT))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Ensure the remote path exists
        try:
            sftp.chdir(REMOTE_PATH)
        except IOError:
            sftp.mkdir(REMOTE_PATH)
            sftp.chdir(REMOTE_PATH)

        # Upload files
        for file_name in os.listdir(local_folder):
            local_path = os.path.join(local_folder, file_name)
            if os.path.isfile(local_path):
                remote_path = os.path.join(REMOTE_PATH, file_name)
                sftp.put(local_path, remote_path)
                logging.info(f"Uploaded {file_name} to {platform}")

        sftp.close()
        transport.close()
    except Exception as e:
        logging.error(f"Error uploading files to {platform}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        logging.error("Usage: python sendSFTP.py <local_folder> <platform>")
        sys.exit(1)

    local_folder = sys.argv[1]
    platform = sys.argv[2]

    if not os.path.exists(local_folder):
        logging.error(f"Local folder '{local_folder}' does not exist.")
        sys.exit(1)

    upload_files(local_folder, platform)
