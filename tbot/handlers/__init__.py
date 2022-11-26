from aiogram import Dispatcher
from aiogram_dialog.exceptions import UnknownIntent
from .error import error_handler
from .like import vote_down_handler, vote_up_handler
from tbot.keyboards.like import vote_cb


def register_all_handlers(dp: Dispatcher):
    dp.register_errors_handler(error_handler, exception=UnknownIntent)
    dp.register_callback_query_handler(vote_up_handler, vote_cb.filter(action='up'))
    dp.register_callback_query_handler(vote_down_handler, vote_cb.filter(action='down'))
