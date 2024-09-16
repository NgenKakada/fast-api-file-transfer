from telebot import TeleBot
from ..core import settings
from app.core.config import settings
import threading

# Use a thread-safe initialization for the bot
bot = None
bot_lock = threading.Lock()

def get_telegram_bot():
    """
    Returns a single instance of the bot, ensuring thread-safety.
    """
    global bot
    if bot is None:
        with bot_lock:
            if bot is None:  # Double check inside the lock
                try:
                    bot = TeleBot(settings.BOT_TOKEN)  # Initialize bot
                except Exception as e:
                    raise ConnectionError(f"Failed to initialize Telegram bot. Error: {str(e)}")
    return bot

def send_telegram_notification(message: str):
    """
    Sends a message to the Telegram channel.
    """
    try:
        bot_instance = get_telegram_bot()  # Get the single bot instance
        bot_instance.send_message(settings.BOT_CHANNEL, message)

        return {"status": "Message sent successfully"}
    except Exception as e:
        # Log the error and return the failure status
        return {"status": "Failed to send message", "error": str(e)}
