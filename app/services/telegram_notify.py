from telebot import TeleBot
from app.core.config import settings

# Initialize the bot with the token from config
bot = TeleBot(settings.BOT_TOKEN)

def send_telegram_notification(message: str):
    """
    Sends a message to the Telegram channel.
    """
    try:
        bot.send_message(settings.BOT_CHANNEL, message)
        return {"status": "Message sent to channel"}
    except Exception as e:
        return {"status": "Failed to send message", "error": str(e)}
