from app.core.sftp_client import SFTPClient
from app.core.config import settings
from app.services.telegram_notify import send_telegram_notification
from datetime import datetime
import os
import re

# Notification tracker to avoid sending multiple notifications
notification_sent = {
    "start": False,
    "success": False,
    "failure": False
}

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by replacing spaces and colons with underscores.
    """
    return re.sub(r'[:\s]', '_', filename)

def generate_file_paths() -> tuple[str, str]:
    """
    Generates the source and destination file paths with a timestamp for the destination file.
    """
    static_filename = "Screenshot 2024-09-13 at 8.28.34 in the morning.png"
    source_file = os.path.join(settings.SOURCE_FILE_DIR, static_filename)
    
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    sanitized_static_filename = sanitize_filename(static_filename)
    
    destination_filename = f"{current_time}_{sanitized_static_filename}"
    destination_file = os.path.join(settings.DESTINATION_FILE_DIR, destination_filename)
    
    return source_file, destination_file

def move_file_between_sftp(source_file_path: str, destination_file_path: str):
    """
    Handles file transfer between two SFTP servers, including notification logic.
    """
    source_sftp = SFTPClient(settings.SOURCE_SFTP_HOST, settings.SOURCE_SFTP_USER, settings.SOURCE_SFTP_PASS)
    destination_sftp = SFTPClient(settings.DESTINATION_SFTP_HOST, settings.DESTINATION_SFTP_USER, settings.DESTINATION_SFTP_PASS)

    global notification_sent
    
    try:
        if not notification_sent["start"]:
            send_telegram_notification(f"Starting file transfer from {source_file_path} to {destination_file_path}")
            notification_sent["start"] = True

        source_sftp.connect()
        destination_sftp.connect()

        if not os.path.exists(settings.TEMPORARY_FILE_DIR):
            os.makedirs(settings.TEMPORARY_FILE_DIR)

        local_temp_file = os.path.join(settings.TEMPORARY_FILE_DIR, os.path.basename(source_file_path))
        source_sftp.get(source_file_path, local_temp_file)
        destination_sftp.put(local_temp_file, destination_file_path)

        if not notification_sent["success"]:
            send_telegram_notification(f"File transfer completed: {source_file_path} -> {destination_file_path}")
            notification_sent["success"] = True

        if os.path.exists(local_temp_file):
            os.remove(local_temp_file)
        
    except Exception as e:
        if not notification_sent["failure"]:
            send_telegram_notification(f"File transfer failed: {source_file_path} -> {destination_file_path}. Error: {str(e)}")
            notification_sent["failure"] = True
        raise e
    
    finally:
        source_sftp.disconnect()
        destination_sftp.disconnect()

        notification_sent["start"] = False
        notification_sent["success"] = False
        notification_sent["failure"] = False
