from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG
###########
# Сижу дома
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
    await message.answer(post['title'])
    await message.answer(post['text'])
    manager.show_mode = ShowMode.SEND
    # await manager.update(manager.data)
    await message.delete()
    await manager.switch_to(StartSG.stayinghome)


async def clean_list_of_read_posts(c: CallbackQuery, button: Button, manager: DialogManager):
    repositories_api.update_user(c.from_user.id, viewed_posts=[])
    await c.answer('Список прочитанных постов очищен')
    await manager.dialog().switch_to(StartSG.start)
# Сижу дома
###########