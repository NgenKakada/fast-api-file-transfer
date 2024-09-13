from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SOURCE_SFTP_HOST: str
    SOURCE_SFTP_USER: str
    SOURCE_SFTP_PASS: str
    DESTINATION_SFTP_HOST: str
    DESTINATION_SFTP_USER: str
    DESTINATION_SFTP_PASS: str
    TEMPORARY_FILE_DIR: str
    BOT_TOKEN: str
    BOT_CHANNEL: str
    SCHEDULER_MINUTE: str
    SCHEDULER_HOUR: str
    SOURCE_FILE_DIR: str
    DESTINATION_FILE_DIR: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    REDIS_PASSWORD: str
        
    class Config:
        env_file = '.env'

def get_settings():
    load_dotenv(override=True)  # Reload the .env file
    return Settings()           # Re-instantiate the settings to reflect new .env values

settings = get_settings()       # Initial load

# Example usage of the function when you want to refresh the configuration
settings = get_settings()
