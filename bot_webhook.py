import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.contrib.fsm_storage import memory, redis
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram_dialog import DialogRegistry

from tbot.config import config
from tbot.handlers import register_all_handlers
from tbot.dialog import start


logging.basicConfig(level=logging.INFO)

if config.redis:
    storage = redis.RedisStorage2(config.redis)
else:
    storage = memory.MemoryStorage()

bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
register_all_handlers(dp)
registy = DialogRegistry(dp)
registy.register_start_handler(start.StartSG.start)
registy.register(start.dialog)
bot['registry'] = registy


async def on_startup(dp):

    await bot.set_webhook(f'{config.webhook_host}{config.webhook_path}')


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.webapp_host,
        port=config.webapp_port
    )
