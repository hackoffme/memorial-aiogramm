from aiogram.types import CallbackQuery,Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG

###########
# Настройки
async def get_settings(c: CallbackQuery | Message, button: Button, manager: DialogManager):
    settings = repositories_api.read_user(c.from_user.id)
    type_settings = [('area_settings', repositories_api.read_area),
                     ('tag_settings', repositories_api.read_tag)]

    for name_settings, repo in type_settings:
        if settings.get('status') == 404:
            settings[name_settings] = repo()
        area_dialog = manager.dialog().find(name_settings)
        for item in settings[name_settings]:
            if isinstance(item, dict):
                item = item['slug']
            await area_dialog.set_checked(event=manager.event, item_id=item, checked=True)
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
