from aiogram import types
from aiogram_dialog import StartMode, ShowMode
from aiogram_dialog.context.stack import DEFAULT_STACK_ID
from aiogram_dialog.manager.bg_manager import BgManager
from tbot.dialog.start import StartSG


async def error_handler(update: types.Update, error):
    id = update.callback_query.from_user.id
    await update.bot.send_message(chat_id=id, text='Меню устарело, держи новое')
    # await update.callback_query.message.delete()
    bg = BgManager(user=update.callback_query.from_user, chat=update.callback_query.message.chat, bot=update.bot,
                   registry=update.bot['registry'], stack_id=DEFAULT_STACK_ID, intent_id=None)
    await bg.start(state=StartSG.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)
    return True


