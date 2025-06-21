import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from handlers import router
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def on_startup(app: web.Application):
    webhook_url = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"
    await bot.set_webhook(webhook_url)
    print(f"Webhook set: {webhook_url}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()
    print("Bot shutdown complete")

async def main():
    app = web.Application()
    app["bot"] = bot
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_shutdown)

    # Обрабатываем только /webhook
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path="/webhook")

    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
