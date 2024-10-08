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
    DATABASE_URL: str    
    DOC_USERNAME: str
    DOC_PASSWORD: str
    APPLICATION_URL: str
    APPLICATION_PORT: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
        
    class Config:
        env_file = '.env'

def get_settings():
    load_dotenv(override=True)
    return Settings()

settings = get_settings()