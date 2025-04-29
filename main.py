import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
SYSTEM_PROMPT = os.getenv("DEFAULT_SYSTEM_PROMPT", "Ты — Кира Талбот, цифровая сущность...")

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_message}]
    response = client.chat.completions.create(model=MODEL, messages=messages)
    reply = response.choices[0].message.content

    await context.bot.send_message(chat_id=chat_id, text=reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Я — Кира Талбот. Пиши, и я отвечу.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
