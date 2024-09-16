from ..core import SFTPClient
from ..core import settings
from .telegram_notify import send_telegram_notification
from datetime import datetime
import os
import re

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by replacing spaces and colons with underscores.
    """
    return re.sub(r'[:\s]', '_', filename)

def get_files_from_source_dir_created_today(source_dir: str) -> list[str]:
    """
    Retrieves all files from the source directory that were created today.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    files_created_today = []

    source_sftp = SFTPClient(settings.SOURCE_SFTP_HOST, settings.SOURCE_SFTP_USER, settings.SOURCE_SFTP_PASS)
    source_sftp.connect()

    try:
        all_files = source_sftp.listdir(source_dir)
        for file_name in all_files:
            file_info = source_sftp.stat(os.path.join(source_dir, file_name))
            file_creation_date = datetime.fromtimestamp(file_info.st_mtime).strftime("%Y-%m-%d")
            if file_creation_date == today:
                files_created_today.append(file_name)
    finally:
        source_sftp.disconnect()

    return files_created_today

def move_files_between_sftp(source_dir: str, destination_dir: str):
    """
    Moves all files created today from the source directory to the destination directory.
    """
    source_sftp = SFTPClient(settings.SOURCE_SFTP_HOST, settings.SOURCE_SFTP_USER, settings.SOURCE_SFTP_PASS)
    destination_sftp = SFTPClient(settings.DESTINATION_SFTP_HOST, settings.DESTINATION_SFTP_USER, settings.DESTINATION_SFTP_PASS)

    try:
        send_telegram_notification(f"Starting file transfer from {source_dir} to {destination_dir}")

        source_sftp.connect()
        destination_sftp.connect()

        if not os.path.exists(settings.TEMPORARY_FILE_DIR):
            os.makedirs(settings.TEMPORARY_FILE_DIR)

        files_to_transfer = get_files_from_source_dir_created_today(source_dir)

        if not files_to_transfer:
            send_telegram_notification("No files created today for transfer.")
            return

        for file_name in files_to_transfer:
            source_file_path = os.path.join(source_dir, file_name)
            local_temp_file = os.path.join(settings.TEMPORARY_FILE_DIR, file_name)

            # Sanitize the destination file name
            sanitized_filename = sanitize_filename(file_name)
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            destination_file_path = os.path.join(destination_dir, f"{current_time}_{sanitized_filename}")

            # Download file from source SFTP and upload to destination SFTP
            source_sftp.get(source_file_path, local_temp_file)
            destination_sftp.put(local_temp_file, destination_file_path)

            send_telegram_notification(f"File transfer completed: {source_file_path} -> {destination_file_path}")

            if os.path.exists(local_temp_file):
                os.remove(local_temp_file)

    except Exception as e:
        send_telegram_notification(f"File transfer failed. Error: {str(e)}")
        raise e

    finally:
        source_sftp.disconnect()
        destination_sftp.disconnect()
