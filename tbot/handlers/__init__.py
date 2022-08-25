from aiogram import Dispatcher
from aiogram_dialog.exceptions import UnknownIntent
from .error import error_handler


def register_all_handlers(dp: Dispatcher):
    dp.register_errors_handler(error_handler, exception=UnknownIntent)
