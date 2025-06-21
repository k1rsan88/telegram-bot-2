import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from handlers import router  # обязательно, иначе Telegram не поймёт команды

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), default=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(router)

async def on_startup(app: web.Application):
    await bot.set_webhook(f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

async def main():
    app = web.Application()

    # Обработка Telegram webhook-запросов
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    setup_application(app, dp, bot=bot)

    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    print(f"Running on http://0.0.0.0:{port}")
    await site.start()

    # Не даём приложению завершиться
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Runtime error: {e}")
