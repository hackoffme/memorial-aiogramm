from aiogram import types
from aiogram.utils.callback_data import CallbackData

vote_cb = CallbackData('vote', 'action', 'post_id') 

def get_keyboard(post_id):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('👍', callback_data=vote_cb.new(action='up', post_id=post_id)),
        types.InlineKeyboardButton('👎🏾', callback_data=vote_cb.new(action='down', post_id=post_id)))