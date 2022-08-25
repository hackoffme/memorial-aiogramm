from aiogram.types import  Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto


from tbot.dialog.stayinghome import stayinghome
from tbot.dialog.wilkingaround import walkingaround, get_location
from tbot.dialog.settings import get_settings


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
