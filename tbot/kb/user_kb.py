from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
key = []
key.append(KeyboardButton('Найти события по близости', request_location=True))
key.append(KeyboardButton('Случайное место'))
key.append(KeyboardButton('О проекте'))


markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(*key)
