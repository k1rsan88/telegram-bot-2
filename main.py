import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from sheets import log_day

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# 🟢 Кнопки при старте
@dp.message(Command("start"))
async def handle_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записать день")],
            [KeyboardButton(text="Посмотреть логи")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Я бот-помощник по учёту дня 🔍", reply_markup=keyboard)

# 🔁 Обработка команды логирования (временно — фиксированные данные)
@dp.message(Command("log"))
async def log_command(message: Message):
    log_day(7.5, "Yes", "Yes", "10:00", "14:00", "Solid session")
    await message.answer("✅ Запись добавлена в Google Таблицу!")

# 🌐 Webhook-режим
async def main():
    await bot.set_webhook(f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook")

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    return app

# 🚀 Запуск
if __name__ == "__main__":
    web.run_app(asyncio.run(main()), host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
