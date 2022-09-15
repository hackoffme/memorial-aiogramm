import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage import redis, memory
from aiogram_dialog import DialogRegistry
from aiogram.types import ParseMode

from tbot.config import config
from tbot.dialog import start
from tbot.handlers import register_all_handlers


async def main():
    if config.redis:
        storage = redis.RedisStorage2(config.redis)
    else:
        storage = memory.MemoryStorage()
    bot = Bot(token=config.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    register_all_handlers(dp)
    registy = DialogRegistry(dp)
    registy.register_start_handler(start.StartSG.start)
    registy.register(start.dialog)
    bot['registry'] = registy
    try:
        await dp.start_polling()
    finally:
        # await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)

