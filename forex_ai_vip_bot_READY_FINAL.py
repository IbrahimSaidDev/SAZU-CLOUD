import os
import logging
import threading
import time
import random
from datetime import datetime
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Bot
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
CHANNEL_ID = os.getenv("CHANNEL_ID","").strip()  # ZABIN - Idan baka saka ba, auto signal bazai tura ba

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "🔥 FOREX AI VIP BOT + AUTO SIGNAL - LIVE 24/7 🔥"

def run_flask():
    port = int(os.getenv("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# === VIP SIGNALS LIST ===
SIGNALS = [
    "🔥 **XAUUSD GOLD**\n📈 BUY @ 2650.00\n🛑 SL: 2642.00\n🎯 TP1: 2658.00\n🎯 TP2: 2665.00\n⏰ H1 - Confidence 85%",
    "📉 **EURUSD**\n📉 SELL @ 1.0850\n🛑 SL: 1.0880\n🎯 TP1: 1.0820\n🎯 TP2: 1.0780\n⏰ M30 - 78%",
    "🔥 **GBPUSD**\n📈 BUY @ 1.2720\n🛑 SL: 1.2680\n🎯 TP1: 1.2760\n🎯 TP2: 1.2800\n⏰ H4 - 82%",
    "⚡️ **BTCUSD**\n📈 BUY @ 67500\n🛑 SL: 66800\n🎯 TP1: 68500\n🎯 TP2: 69500\n🤖 Strong Uptrend",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 VIP SIGNALS", callback_data='vip')],
        [InlineKeyboardButton("🤖 FOREX AI ANALYSIS", callback_data='ai')],
        [InlineKeyboardButton("💬 SUPPORT", url="https://t.me/IbrahimSaidDev")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔥 *FOREX AI VIP BOT - LIVE* 🔥\n\nBarka da zuwa Ibrahim!\nBot dinka yana aiki 24/7 akan Render ✅\n\nAuto Signal zai tura a channel dinka kowane 4 hours 🔥\n\nZaba daga kasa:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'vip':
        sig = random.choice(SIGNALS)
        await query.edit_message_text(f"✅ *VIP SIGNAL:*\n\n{sig}\n\n🕐 {datetime.now().strftime('%H:%M')}", parse_mode='Markdown')
    elif query.data == 'ai':
        await query.edit_message_text("🤖 AI Analysis: Market yana Bullish yau! Gold zai tashi zuwa 2660 🔥")

# === AUTO SIGNAL SENDER 24/7 ===
async def send_auto_signal(bot_token, channel_id):
    bot = Bot(token=bot_token)
    signal = random.choice(SIGNALS)
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    message = f"{signal}\n\n🕐 {now} WAT\n🤖 Powered by FOREX AI VIP\n✅ BOT LIVE 24/7"
    try:
        await bot.send_message(chat_id=channel_id, text=message, parse_mode='Markdown')
        logger.info(f"✅ Auto Signal tura zuwa {channel_id}")
    except Exception as e:
        logger.error(f"❌ Channel Error: {e} - Tabbatar bot admin ne a channel!")

def auto_signal_loop():
    if not CHANNEL_ID:
        logger.info("CHANNEL_ID baya nan - Auto signal ba zai tura ba (amma /start zai yi aiki)")
        return
    while True:
        try:
            time.sleep(60)  # Jira 1 min bayan fara bot
            asyncio.run(send_auto_signal(BOT_TOKEN, CHANNEL_ID))
            logger.info("⏳ Jiran 4 hours...")
            time.sleep(14400)  # 4 hours - canza zuwa 3600 = 1 hour
        except Exception as e:
            logger.error(f"Loop error: {e}")
            time.sleep(60)

def main():
    keep_alive()
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN baya nan!")
        while True: time.sleep(60)

    # Fara auto signal thread (24/7)
    t = threading.Thread(target=auto_signal_loop)
    t.daemon = True
    t.start()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot + Auto Signal LIVE 24/7")
    app.run_polling()

if __name__ == "__main__":
    main()
