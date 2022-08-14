import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

from tbot.config import config
from tbot.handlers.user import register_user
from tbot.kb.dialog import start


def register_all_handlers(dp):
    register_user(dp)


async def main():
    storage = MemoryStorage()
    bot = Bot(token=config.token, parse_mode='HTML')
    # bot['hi'] = repositories_api.get_hi()
    dp = Dispatcher(bot, storage=storage)

    # register_all_handlers(dp)

    registy = DialogRegistry(dp)
    registy.register_start_handler(start.StartSG.start)#, text="/start", state="*")
    registy.register(start.dialog)
    # registy.register(settings.settings)
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)
