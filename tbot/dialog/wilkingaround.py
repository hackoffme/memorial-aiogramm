from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG
from tbot.dialog.stayinghome import stayinghome, clean_list_of_read_posts

###########
# Иду ногами
async def walkingaround(c: CallbackQuery | Message, button: Button, manager: DialogManager):
    # await c.answer()
    # await c.message.delete()
    key = KeyboardButton(
        '🌍Нажмите сюда, чтобы отправить свою геолокацию', request_location=True)
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(key)

    message = c.message if hasattr(c, 'message') else c

    await message.answer('Если мы будем знать Ваше местоположение, то сможешь найти интересную статью о событиях происходивших поблизости', reply_markup=markup)


async def walkingaround_show_more(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer()
    q = repositories_api.read_post_by_saved_coordinates(c.from_user.id)
    if q['status']!=200:
        await c.message.answer('Нет статей для отображения. Измените условия поиска, либо вы находитесь далеко от локаций')
        return

    await c.message.answer(q['title'])
    await c.message.answer(q['text'])
    await c.message.answer('Получили еще статейку. Координаты уже в БД. Логику поиска статьи надо сделать')
    manager.show_mode = ShowMode.SEND
# Иду ногами
 ###########

