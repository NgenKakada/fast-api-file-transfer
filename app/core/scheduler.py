from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from app.services.file_transfer import move_file_between_sftp, generate_file_paths
from app.core.config import settings
from redis import Redis

# Redis configuration
redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)

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
    """
    Acquires a Redis lock and runs the file transfer job.
    """
    source_file, destination_file = generate_file_paths()
    lock = redis_conn.lock('file_transfer_lock', timeout=60)
    lock_acquired = False

    try:
        lock_acquired = lock.acquire(blocking=False)
        if lock_acquired:
            move_file_between_sftp(source_file, destination_file)
    finally:
        if lock_acquired:
            lock.release()

# Schedule the file transfer job
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

# Context manager to manage scheduler shutdown
@asynccontextmanager
async def lifespan(app):
    yield
    scheduler.shutdown()
