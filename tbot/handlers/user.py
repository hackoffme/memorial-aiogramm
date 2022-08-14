from aiogram import Dispatcher, types
from aiogram.types import Message

from tbot.kb.user_kb import markup




async def stayinghome(callback_query: types.CallbackQuery):
    await callback_query.message.answer('/start')
    await callback_query.answer()
    

async def walkingaround(callback_query: types.CallbackQuery):
    await callback_query.message.answer('/start')
    

async def options(callback_query: types.CallbackQuery):
    await callback_query.message.answer('/start')
    


# start
async def user_start(message: Message):
    print('ata')
    await message.answer(message.bot.get("hi"), reply_markup=markup)


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
    dp.register_callback_query_handler(stayinghome, lambda c: c.data == 'stayinghome')
    dp.register_callback_query_handler(walkingaround, lambda c: c.data == 'walkingaround')
    dp.register_callback_query_handler(options, lambda c: c.data == 'options')
    dp.register_message_handler(user_start,
                            commands=["start", "help"])
    dp.register_message_handler(get_location,
                            content_types=types.ContentTypes.LOCATION)
    dp.register_edited_message_handler(edit_live_location,
                                   content_types=types.ContentTypes.LOCATION)
