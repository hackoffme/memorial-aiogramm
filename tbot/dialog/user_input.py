from aiogram.types import  Message, ReplyKeyboardRemove

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG
from tbot.dialog.stayinghome import stayinghome
from tbot.dialog.wilkingaround import walkingaround
from tbot.dialog.settings import get_settings

###########
# Обработка пользовательского ввода
async def get_location(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    await m.answer(m.location, reply_markup=ReplyKeyboardRemove())
    await m.answer('Здесь получаем и выводим пост. Логику поиска надо обсудить... Вот бы прогуляться по этому каналу.  Координаты бы куда засейвить')
    q = repositories_api.read_post_by_coordinates(
        m.from_id, m.location.latitude, m.location.longitude)
    if q['status'] != 200:
        await m.answer('Нет статей для отображения. Измените условия поиска, либо вы находитесь далеко от локаций')
        return
    await m.answer(q['title'])
    await m.answer(q['text'])
    await manager.switch_to(StartSG.walkingaround)


async def messange_input(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    commands = {'/stayinghome': stayinghome, '/walkingaround': walkingaround,
                '/options': get_settings, '/stories': stayinghome}

    if 'location' in m:
        await get_location(m, dialog, manager)
    if 'text' in m:
        if m.text.lower() in commands:
            await commands[m.text.lower()](m, dialog, manager)
        else:
            await m.delete()
            manager.show_mode = ShowMode.EDIT
# Обработка пользовательского ввода
 ###########
