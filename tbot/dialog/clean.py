from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG


async def clean_list_of_read_posts(c: CallbackQuery, button: Button, manager: DialogManager):
    repositories_api.update_user(c.from_user.id, viewed_posts=[])
    await c.answer('Список прочитанных постов очищен')
    await manager.dialog().switch_to(StartSG.start)