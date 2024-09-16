from telebot import TeleBot
from ..core import settings

# Initialize the bot globally to ensure it's only initialized once
bot = None

def get_telegram_bot():
    """
    Returns a single instance of the bot.
    """
    global bot
    if bot is None:
        bot = TeleBot(settings.BOT_TOKEN)  # Initialize bot only if it hasn't been initialized yet
    return bot

def send_telegram_notification(message: str):
    """
    Sends a message to the Telegram channel.
    """
    try:
        bot_instance = get_telegram_bot()  # Get the single bot instance
        bot_instance.send_message(settings.BOT_CHANNEL, f"{message}")
        
        return {"status": "Message sent to channel"}
    except Exception as e:
        return {"status": "Failed to send message", "error": str(e)}
