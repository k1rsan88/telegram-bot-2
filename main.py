import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import router

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), default=ParseMode.HTML)  # Исправлено здесь
dp = Dispatcher()
dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
