from fastapi import FastAPI
from app.routers import sftp

app = FastAPI()

app.include_router(sftp.router, prefix="/sftp")