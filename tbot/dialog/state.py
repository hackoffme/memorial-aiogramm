from aiogram.dispatcher.filters.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    stayinghome = State()
    walkingaround = State()
    settings_area = State()
    settings_tag = State()
    settings_reset = State()
