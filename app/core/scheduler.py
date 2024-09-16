from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
<<<<<<< HEAD
from ..core import settings
=======
from app.services.file_transfer import move_files_between_sftp
from app.core.config import settings
>>>>>>> develop
from redis import Redis
import logging

# Setup logging for job-related activities
logger = logging.getLogger(__name__)

# Redis configuration
redis_conn = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    socket_timeout=5,  # Adding timeout to avoid long waiting
    retry_on_timeout=True
)

# Setup RedisJobStore
jobstores = {
    'default': RedisJobStore(
        jobs_key='apscheduler_jobs',
        run_times_key='apscheduler_run_times',
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD
    )
}

# Initialize scheduler with RedisJobStore
scheduler = BackgroundScheduler(jobstores=jobstores)

# Load scheduler config from .env
scheduler_minute = settings.SCHEDULER_MINUTE
scheduler_hour = settings.SCHEDULER_HOUR

def run_job_with_lock():
    from ..services import move_file_between_sftp, generate_file_paths
    """
    Acquires a Redis lock and runs the file transfer job for all files created today.
    """
    lock = redis_conn.lock('file_transfer_lock', timeout=60)
    lock_acquired = False

    try:
        # Attempt to acquire lock without blocking
        lock_acquired = lock.acquire(blocking=False)
        if lock_acquired:
            logger.info("Lock acquired. Starting file transfer job.")
            # Moving files between SFTP without generating specific file paths
            move_files_between_sftp(settings.SOURCE_FILE_DIR, settings.DESTINATION_FILE_DIR)
            logger.info("File transfer job completed.")
        else:
            logger.warning("Could not acquire lock. Another instance might be running.")
    except Exception as e:
        logger.error(f"Error during file transfer job: {str(e)}", exc_info=True)
    finally:
        if lock_acquired:
            lock.release()
            logger.info("Lock released.")

# Schedule the file transfer job
job_id = "file_transfer_job"
scheduler.add_job(
    run_job_with_lock,
    CronTrigger(minute=scheduler_minute, hour=scheduler_hour),
    id=job_id,
    replace_existing=True,
    max_instances=1,
    misfire_grace_time=300,  # Allow 5 minutes of grace for misfired jobs
    coalesce=True  # Combine multiple missed executions into one
)

# Start the scheduler
scheduler.start()

# Context manager to manage scheduler shutdown
@asynccontextmanager
async def lifespan(app):
    yield
    logger.info("Shutting down scheduler.")
    scheduler.shutdown()
