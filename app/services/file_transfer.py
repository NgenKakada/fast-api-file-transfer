from app.core.sftp_client import SFTPClient
from app.core.config import settings
from app.services.telegram_notify import send_telegram_notification
import os

def move_file_between_sftp(source_file_path: str, destination_file_path: str):
    # Initialize SFTP clients
    source_sftp = SFTPClient(settings.SOURCE_SFTP_HOST, settings.SOURCE_SFTP_USER, settings.SOURCE_SFTP_PASS)
    destination_sftp = SFTPClient(settings.DESTINATION_SFTP_HOST, settings.DESTINATION_SFTP_USER, settings.DESTINATION_SFTP_PASS)
    
    try:
        # Send notification before starting the transfer
        send_telegram_notification(f"Starting file transfer from {source_file_path} to {destination_file_path}")

        # Connect to SFTP servers
        source_sftp.connect()
        destination_sftp.connect()

        # Ensure the TEMPORARY_FILE_DIR exists
        if not os.path.exists(settings.TEMPORARY_FILE_DIR):
            os.makedirs(settings.TEMPORARY_FILE_DIR)

        # Define a temporary local file path
        local_temp_file = os.path.join(settings.TEMPORARY_FILE_DIR, os.path.basename(source_file_path))
        
        # Download file from source SFTP
        source_sftp.get(source_file_path, local_temp_file)
        
        # Upload file to destination SFTP
        destination_sftp.put(local_temp_file, destination_file_path)
        
        # Send success notification after transfer completes
        send_telegram_notification(f"File transfer completed: {source_file_path} -> {destination_file_path}")

        # Optionally, clean up the local temp file after the operation
        if os.path.exists(local_temp_file):
            os.remove(local_temp_file)
        
    except Exception as e:
        # Send failure notification if something goes wrong
        send_telegram_notification(f"File transfer failed: {source_file_path} -> {destination_file_path}. Error: {str(e)}")
        raise e
    
    finally:
        # Disconnect from SFTP servers
        source_sftp.disconnect()
        destination_sftp.disconnect()
