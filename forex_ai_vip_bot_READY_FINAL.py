import os
import logging
import threading
import time
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "🔥 FOREX AI VIP BOT - LIVE 24/7 🔥"

def run_flask():
    port = int(os.getenv("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 VIP SIGNALS", callback_data='vip')],
        [InlineKeyboardButton("🤖 AI ANALYSIS", callback_data='ai')],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔥 FOREX AI VIP BOT LIVE 24/7! Zaba:", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'vip':
        await query.edit_message_text("✅ VIP: XAUUSD BUY 2650 SL 2645 TP 2660")
    else:
        await query.edit_message_text("🤖 AI: Market Bullish yau!")

def main():
    keep_alive()
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN baya nan!")
        while True:
            time.sleep(60)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot LIVE 24/7")
    app.run_polling()

if __name__ == "__main__":
    main()
