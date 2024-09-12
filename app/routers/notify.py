from fastapi import APIRouter
from app.services.telegram_notify import send_telegram_notification

router = APIRouter()

@router.post("/notify")
async def notify(message: str):
    response = send_telegram_notification(message)
    return response