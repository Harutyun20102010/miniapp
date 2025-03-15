import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7627730398:AAFjp1_sGvu8ro9r2uZU0qdbLnYQFMdxU_g"
GAME_URL = "t.me/hayem_store_bot/HayMining"  # Replace with your game URL

# Flask server to keep the bot alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Create the message text with emojis
    message_text = (
        f"🌟 Hello, {user.first_name}! 🌟\n\n"
        "💎 The first Armenian application for mining!\n\n"
        "🚀 Why Choose Hay Mining?\n"
        "✅ Easy to Use: Start mining in just a few clicks!\n"
        "✅ Fast & Secure: Your earnings are safe with us.\n"
        "✅ Earn Real Money: Turn your time into profit!\n\n"
        "👉 Press the button below to start mining and earn rewards! 🎮"
    )

    # Create an inline keyboard
    keyboard = [
        [InlineKeyboardButton("🎮 Start Mining Now", url=f"{GAME_URL}?username={user.username}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline keyboard
    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to play the game.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    # Start the Flask server to keep the bot alive
    keep_alive()

    # Initialize the Telegram bot
    app_bot = Application.builder().token(TOKEN).build()

    # Add command handlers
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_command))

    # Add error handler
    app_bot.add_error_handler(error_handler)

    # Start the bot
    app_bot.run_polling()

if __name__ == "__main__":
    main()