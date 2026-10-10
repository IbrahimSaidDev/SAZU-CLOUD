import os
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL", "@ForexAiVip")

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
        [InlineKeyboardButton("🤖 FOREX AI ANALYSIS", callback_data='ai')],
        [InlineKeyboardButton("💬 SUPPORT", url="https://t.me/IbrahimSaidDev")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔥 *FOREX AI VIP BOT - LIVE* 🔥\n\n"
        "Barka da zuwa Ibrahim!\n"
        "Bot dinka yana aiki 24/7 akan Render ✅\n\n"
        "Zaba daga kasa:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'vip':
        await query.edit_message_text("✅ VIP Signals suna tafe! XAUUSD BUY 2650 SL 2645 TP 2660")
    elif query.data == 'ai':
        await query.edit_message_text("🤖 AI Analysis: Market yana Bullish yau, jira Buy setup a London session!")

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN baya nan! Saka shi a Render > Environment")
        return
    keep_alive()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot na tashi... LIVE 24/7")
    app.run_polling()

if __name__ == "__main__":
    main()
