from email.errors import MessageError
from aiogram import Dispatcher, types
from aiogram.types import Message

from tbot.kb.user_kb import markup


async def user_start(message: Message):
    await message.reply('Привет, друг. Если ты гуляешь по Волго-Донскому каналу,'
                        'то отправив свою локацию можешь узнать'
                        'о событиях, происходивших рядом с твоей локацией',
                        reply_markup=markup)


async def get_location(message: Message):
    await message.answer(message)
    await message.answer(message.location)
    if message.location.live_period:
        await message.answer(f'время доступа к координатам {message.location.live_period} секунд, в'
                             'в минутах гораздо меньше')


# Ловим редактирование координат
async def edit_live_location(message: Message):
    await get_location(message)


# Регистрируем все обработчики команд
def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(
        get_location, content_types=types.ContentTypes.LOCATION)
    dp.register_edited_message_handler(
        edit_live_location, content_types=types.ContentTypes.LOCATION)
