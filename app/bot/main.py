import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.handlers.user import router, bot

dp = Dispatcher()

storage = MemoryStorage()

dp.include_router(router)

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())