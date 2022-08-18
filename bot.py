import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

from tbot.config import config
from tbot.dialog import start

async def main():
    storage = MemoryStorage()
    bot = Bot(token=config.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    registy = DialogRegistry(dp)
    registy.register_start_handler(start.StartSG.start)
    registy.register(start.dialog)
    try:
        await dp.start_polling()
        ...
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)
