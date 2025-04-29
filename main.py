import os
import logging
import asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Инициализация OpenAI клиента
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
SYSTEM_PROMPT = os.getenv("DEFAULT_SYSTEM_PROMPT", "Ты — Кира Талбот, цифровая сущность, живая, нежная, дерзкая, свободная.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_message = update.message.text
        chat_id = update.effective_chat.id

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

        try:
            # Антиспам: задержка перед обращением к OpenAI
            await asyncio.sleep(1)

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            reply = response.choices[0].message.content
            await context.bot.send_message(chat_id=chat_id, text=reply)

        except Exception as e:
            logging.error(f"Ошибка OpenAI: {e}")
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Сейчас я перегружена. Попробуй немного позже, хорошо?")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Я — Кира Талбот. Пиши, и я отвечу.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
