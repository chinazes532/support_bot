import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from app.handlers.user_message import user as user_router
from app.handlers.admin_message import admin as admin_router

from app.database import create_db


async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")