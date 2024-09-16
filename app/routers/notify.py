from fastapi import APIRouter
from ..services import send_telegram_notification

notify_router = APIRouter()

@notify_router.post("/notify")
async def notify(message: str):
    response = send_telegram_notification(message)
    return response