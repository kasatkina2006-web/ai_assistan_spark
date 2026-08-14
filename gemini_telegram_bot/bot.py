import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.getenv("PORT", 8080))

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Не найдены переменные TELEGRAM_BOT_TOKEN или GEMINI_API_KEY")

# Инициализация Gemini
genai.configure(api_key=GEMINI_API_KEY)

def init_gemini_model():
    """Автоматический поиск доступной модели Gemini для вашего ключа"""
    try:
        available = [
            m.name for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        # Ищем доступную flash-модель (gemini-2.5-flash, gemini-2.0-flash и т.д.)
        for name in available:
            if "flash" in name.lower() and "preview" not in name.lower():
                print(f"Используем модель: {name}")
                return genai.GenerativeModel(name)
        # Если flash нет, берем первую доступную
        if available:
            print(f"Используем модель: {available[0]}")
            return genai.GenerativeModel(available[0])
    except Exception as e:
        print(f"Ошибка получения списка моделей: {e}")
    return genai.GenerativeModel("gemini-2.0-flash")

model = init_gemini_model()

# Инициализация Telegram-бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Напишите мне вопрос, и я отвечу с помощью Gemini.")

@dp.message()
async def message_handler(message: types.Message):
    if not message.text:
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    global model
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        # Если модель выдала сбой, пробуем переподключить активную модель
        try:
            model = init_gemini_model()
            response = model.generate_content(message.text)
            await message.answer(response.text)
        except Exception as retry_err:
            await message.answer(f"Ошибка при обработке запроса: {retry_err}")

# Микро-сервер для проверки статуса на Render
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

async def main():
    print(f"Запуск веб-сервера на порту {PORT} и запуск бота...")
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
