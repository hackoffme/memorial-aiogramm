from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Message, ReplyKeyboardRemove

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG
from tbot.dialog.utils import send_post


async def walkingaround(c: CallbackQuery | Message, button: Button, manager: DialogManager):
    key = KeyboardButton(
        '🌍Нажмите сюда, чтобы отправить свою геолокацию', request_location=True)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(key)
    message = c.message if hasattr(c, 'message') else c
    await message.answer('Если мы будем знать Ваше местоположение, то сможешь найти интересную статью о событиях происходивших поблизости', reply_markup=markup)


async def get_location(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    await m.answer('Мы получили Вашу локацию', reply_markup=ReplyKeyboardRemove())
    post = repositories_api.read_post_by_coordinates(
        m.from_id, m.location.latitude, m.location.longitude)
    if post['status'] != 200:
        await m.answer('Нет статей для отображения. Измените условия поиска, либо вы находитесь далеко от локаций')
        return
    await send_post(m, post)
    await manager.switch_to(StartSG.walkingaround)


async def walkingaround_show_more(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer()
    post = repositories_api.read_post_by_saved_coordinates(c.from_user.id)
    if post['status']!=200:
        await c.message.answer('Нет статей для отображения. Измените условия поиска, либо вы находитесь далеко от локаций')
        return
    await send_post(c.message, post)
    manager.show_mode = ShowMode.SEND


