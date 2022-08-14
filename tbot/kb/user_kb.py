from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




class CheckBoxInline(InlineKeyboardButton):
    def __init__(self, check=False, *args, **kwargs):
        super().__init__(args, **kwargs)
        self.check = check

key = []

key.append(InlineKeyboardButton('Сижу дома', callback_data='stayinghome'))
key.append(InlineKeyboardButton('Иду ногами', callback_data='walkingaround'))
key.append(InlineKeyboardButton('Настройки', callback_data='options'))

markup = InlineKeyboardMarkup()
markup.add(*key)

