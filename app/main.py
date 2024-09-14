from fastapi import FastAPI
from app.routers import product, sftp
from app.core.scheduler import lifespan  # Import the lifespan function from scheduler.py

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)  # Attach lifespan to the app

# Include routers (sftp, notify, etc.)
app.include_router(sftp.router, prefix="/sftp")

# Include routers (sftp, notify, etc.)
app.include_router(product.router, prefix="/products")
