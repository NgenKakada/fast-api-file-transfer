from app.core.sftp_client import SFTPClient
from app.core.config import settings
import os

def move_file_between_sftp(source_file_path: str, destination_file_path: str):
    source_sftp = SFTPClient(settings.SOURCE_SFTP_HOST, settings.SOURCE_SFTP_USER, settings.SOURCE_SFTP_PASS)
    destination_sftp = SFTPClient(settings.DESTINATION_SFTP_HOST, settings.DESTINATION_SFTP_USER, settings.DESTINATION_SFTP_PASS)
    
    try:
        source_sftp.connect()
        destination_sftp.connect()

        # Ensure the TEMPORARY_FILE_DIR exists, create it if it doesn't
        if not os.path.exists(settings.TEMPORARY_FILE_DIR):
            os.makedirs(settings.TEMPORARY_FILE_DIR)

        # Define a temporary local file path
        local_temp_file = os.path.join(settings.TEMPORARY_FILE_DIR, os.path.basename(source_file_path))
        
        # Download file from source_sftp
        source_sftp.get(source_file_path, local_temp_file)  # 'get' method downloads the file
        
        # Upload file to destination_sftp
        destination_sftp.put(local_temp_file, destination_file_path)  # 'put' method uploads the file
        
        # Optionally, clean up the local temp file after the operation
        if os.path.exists(local_temp_file):
            os.remove(local_temp_file)
        
    finally:
        source_sftp.disconnect()
        destination_sftp.disconnect()
