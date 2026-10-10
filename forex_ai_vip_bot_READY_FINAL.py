import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📈 VIP SIGNALS", callback_data='vip')],[InlineKeyboardButton("🤖 FOREX AI ANALYSIS", callback_data='ai')],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔥 FOREX AI VIP BOT - LIVE 🔥\nBarka da zuwa!", reply_markup=reply_markup)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ VIP Signal: XAUUSD BUY")
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
if __name__ == "__main__":
    main()
