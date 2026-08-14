# Gemini Telegram Bot

Telegram-бот с искусственным интеллектом на базе Google Gemini API, готовый для развертывания на Render.

## Установка и локальный запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <URL_РЕПОЗИТОРИЯ>
   cd gemini_telegram_bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` и укажите ключи:
   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   GEMINI_API_KEY=ваш_ключ_gemini
   PORT=8080
   ```

4. Запустите бота:
   ```bash
   python bot.py
   ```

## Развертывание на Render

1. Загрузите проект в репозиторий на GitHub.
2. Создайте новый **Web Service** на [Render](https://render.com/).
3. Настройте параметры:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
4. В разделе **Environment Variables** добавьте:
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY`
