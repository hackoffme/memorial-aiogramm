import asyncio
from aiogram import Bot, Dispatcher

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

from tbot.models.database import Base
from tbot.models.locate import Locate
from tbot.config import load_config
from tbot.handlers.user import register_user


def register_all_handlers(dp):
    register_user(dp)


# async def on_startup():
#     print('start')


async def main():
    config = load_config(".env")

    # engine = create_async_engine(f'sqlite+aiosqlite:///db.sqlite')

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    # async_sessionmaker = sessionmaker(
    #     engine, expire_on_commit=False, class_=AsyncSession
    # )

    bot = Bot(token=config.token, parse_mode='HTML')
    dp = Dispatcher(bot)
    # dp['db'] = async_sessionmaker

    # await Locate.add_fake_data(async_sessionmaker())

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)
