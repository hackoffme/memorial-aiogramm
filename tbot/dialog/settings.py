from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG



async def get_settings(c: CallbackQuery | Message, button: Button, manager: DialogManager):
    user = repositories_api.read_user(c.from_user.id)
    if user.status != 200:
        user = repositories_api.create_user(c.from_user.id)
    area_dialog = manager.dialog().find('area_settings')
    for item in user.area_settings:
        await area_dialog.set_checked(event=manager.event, item_id=item, checked=True)
    
    tag_dialog = manager.dialog().find('tag_settings')
    for item in user.tag_settings:
        await tag_dialog.set_checked(event=manager.event, item_id=item, checked=True)
    
    await manager.dialog().switch_to(StartSG.settings_area)



async def settings_end(c: CallbackQuery, button: Button, manager: DialogManager):
    dialog = manager.dialog()
    checked_area = dialog.find('area_settings').get_checked()
    checked_tag = dialog.find('tag_settings').get_checked()
    q = repositories_api.update_user(
        c.from_user.id, tag_settings=checked_tag, area_settings=checked_area)
    await manager.dialog().switch_to(StartSG.start)
# Настройки
###########
