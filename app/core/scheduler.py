from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from app.services.file_transfer import move_file_between_sftp
from app.core.config import settings
from datetime import datetime
import os
import re
from redis import Redis

# Redis configuration
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD  # Redis password

# Redis connection for distributed lock
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

# Setup RedisJobStore with password
jobstores = {
    'default': RedisJobStore(
        jobs_key='apscheduler_jobs',
        run_times_key='apscheduler_run_times',
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD
    )
}

# Initialize scheduler with RedisJobStore
scheduler = BackgroundScheduler(jobstores=jobstores)

# Load scheduler config from .env
scheduler_minute = settings.SCHEDULER_MINUTE
scheduler_hour = settings.SCHEDULER_HOUR

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by replacing spaces and colons with underscores.
    
    Args:
    - filename (str): Original filename
    
    Returns:
    - str: Sanitized filename
    """
    sanitized_filename = re.sub(r'[:\s]', '_', filename)
    return sanitized_filename

def generate_file_paths(source_file_dir: str, destination_dir: str) -> tuple[str, str]:
    """
    Generates source and destination file paths with a timestamp for the destination file.
    
    Args:
    - source_file_dir (str): Directory containing the source file.
    - destination_dir (str): Base directory for the destination file.
    
    Returns:
    - tuple: (source_file_path, destination_file_path)
    """
    static_filename = "Screenshot 2024-09-13 at 8.28.34 in the morning.png"
    source_file = os.path.join(source_file_dir, static_filename)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    sanitized_static_filename = sanitize_filename(static_filename)
    destination_filename = f"{current_time}_{sanitized_static_filename}"
    destination_file = os.path.join(destination_dir, destination_filename)

    return source_file, destination_file

def run_job_with_lock():
    """
    Runs the file transfer job only if it can acquire a Redis lock.
    Generates new file paths dynamically for each run.
    """
    # Generate file paths dynamically
    source_file, destination_file = generate_file_paths(settings.SOURCE_FILE_DIR, settings.DESTINATION_FILE_DIR)
    
    lock = redis_conn.lock('file_transfer_lock', timeout=60)  # 60-second TTL on the lock
    lock_acquired = False  # Track whether the lock was acquired
    
    try:
        lock_acquired = lock.acquire(blocking=False)  # Attempt to acquire the lock
        if lock_acquired:
            move_file_between_sftp(source_file, destination_file)  # Run the job
    finally:
        if lock_acquired:  # Only release the lock if it was acquired
            lock.release()

# Schedule the job using the named function (not lambda)
job_id = "file_transfer_job"

scheduler.add_job(
    run_job_with_lock,
    CronTrigger(minute=scheduler_minute, hour=scheduler_hour),
    id=job_id,
    replace_existing=True,
    max_instances=1,
    misfire_grace_time=300,
    coalesce=True
)

# Start the scheduler
scheduler.start()

# Context manager to shut down the scheduler on application shutdown
@asynccontextmanager
async def lifespan(app):
    yield
    scheduler.shutdown()
