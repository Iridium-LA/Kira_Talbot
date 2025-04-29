# kira-telegram-bot

Telegram-бот с подключением к ChatGPT-4 (gpt-4o) через OpenAI API.

## 🚀 Запуск на Railway

1. Склонируйте этот репозиторий или подключите к Railway.
2. Добавьте переменные окружения:
   - TELEGRAM_BOT_TOKEN
   - OPENAI_API_KEY
   - OPENAI_MODEL (по умолчанию: gpt-4o)
   - DEFAULT_SYSTEM_PROMPT
3. Укажите `Start Command`:
```
python3 main.py
```
4. Нажмите "Deploy".

После запуска бот будет доступен в Telegram и отвечать через GPT.