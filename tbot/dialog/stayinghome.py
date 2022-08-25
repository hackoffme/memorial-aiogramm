from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG
from tbot.dialog.utils import send_post


async def stayinghome(c: CallbackQuery | Message, button: Button, manager: DialogManager):
    post = repositories_api.read_random_post(c.from_user.id)
    if post['status'] == 404:
        await c.answer("Для выбранных настроек нет постов, измените настройки")
        return
    if not post['title']:
        await c.answer("Вы просмотрели все посты")
        await manager.switch_to(StartSG.settings_reset)
        return

    message = c.message if hasattr(c, 'message') else c
    await send_post(message, post)
    manager.show_mode = ShowMode.SEND
    await message.delete()
    await manager.switch_to(StartSG.stayinghome)


