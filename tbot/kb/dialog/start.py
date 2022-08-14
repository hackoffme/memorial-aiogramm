from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from aiogram_dialog import DialogManager, Dialog, Window, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Group, Multiselect, ManagedMultiSelectAdapter, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja

from tbot.repositories import repositories_api


async def get_data(*args, **kwargs):
    # Геттер для диалога
    area = repositories_api.read_area()
    tag = repositories_api.read_tag()
    hi = repositories_api.get_hi()
    return {'area_settings': area, 'tag_settings': tag, 'hi': hi}


async def stayinghome(c: CallbackQuery, button: Button, manager: DialogManager):
    post = repositories_api.read_random_post(c.from_user.id)
    if post['status'] == 404:
        await c.answer("Для выбранных настроек нет постов, измените настройки")
        return
    if not post['title']:
        await c.answer("Вы просмотрели все посты")
        await manager.switch_to(StartSG.settings_reset)
        return
    await c.message.answer(post['title'])
    await c.message.answer(post['text'])
    manager.show_mode = ShowMode.SEND
    await c.message.delete()
    await manager.switch_to(StartSG.stayinghome)


async def walkingaround(c: CallbackQuery, button: Button, manager: DialogManager):
    key=(InlineKeyboardButton('Иду ногами', callback_data='walkingaround'))
    # key=(InlineKeyboardButton('Иду ногами', callback_data='walkingaround'))
    markup = InlineKeyboardMarkup()
    markup.add(key)
    await c.message.answer('sf', reply_markup=markup)


async def get_settings(c: CallbackQuery, button: Button, manager: DialogManager):
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


async def settings_tag(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(StartSG.settings_tag)


async def settings_end(c: CallbackQuery, button: Button, manager: DialogManager):
    dialog = manager.dialog()
    checked_area = dialog.find('area_settings').get_checked()
    checked_tag = dialog.find('tag_settings').get_checked()
    q = repositories_api.update_user(
        c.from_user.id, tag_settings=checked_tag, area_settings=checked_area)
    if q == 404:
        repositories_api.create_user(c.from_user.id, checked_tag, checked_area)
    await manager.dialog().switch_to(StartSG.start)


async def clean_list_of_read_posts(c: CallbackQuery, button: Button, manager: DialogManager):
    repositories_api.update_user(c.from_user.id, viewed_posts=[])
    await c.answer('Список прочитанных постов очищен')
    await manager.dialog().switch_to(StartSG.start)


class StartSG(StatesGroup):
    start = State()
    stayinghome = State()
    walkingaround = State()
    settings_area = State()
    settings_tag = State()
    settings_reset = State()


dialog = Dialog(
    Window(
        Format("{hi}"),
        Row(
            Button(Const("Сижу дома"), id="stayinghome",
                   on_click=stayinghome),
            Button(Const("Иду ногами"), id="walkingaround",
                   on_click=walkingaround),
            Button(Const("Настройки"), id="options",
                   on_click=get_settings),

        ),
        state=StartSG.start,
    ),
    Window(
        Format("Хотите больше, нажмите показать статью"),
        Row(
            SwitchTo(Const('Назад'), id='back', state=StartSG.start),
            Button(Const('Показать еще статью'),
                   id="im_lucky", on_click=stayinghome),
        ),
        state=StartSG.stayinghome
    ),

    # Window(
    #     Format("Привет! Сейчас возьму информацию о твоем местоположении, согласен?"),
    #     Row(
    #         SwitchTo(Const('Назад'), id='back', state=StartSG.start),
    #         Button(Const('ДА'),
    #                id="get_location", on_click=walkingaround),
    #     ),
    #     state=StartSG.walkingaround
    # ),
    Window(
        Format("Привет! это мои настройки. Выберите район поиска:"),
        Group(Multiselect(
            Jinja('✅ {{item["title"]}}'),
            Jinja('❌ {{item["title"]}}'),
            id="area_settings",
            item_id_getter=lambda x: x['slug'],
            items='area_settings'
        ),
            width=2
        ),
        Button(Const("Далее"), id="next_settings", on_click=settings_tag),
        state=StartSG.settings_area
    ),
    Window(
        Format("Выберите теги, которые вым интересны"),
        Group(Multiselect(
            Jinja('✅ {{item["title"]}}'),
            Jinja('❌ {{item["title"]}}'),
            id="tag_settings",
            item_id_getter=lambda x: x['slug'],
            items='tag_settings'
        ),
            width=2
        ),
        Button(Const("Далее"), id="end_settings", on_click=settings_end),
        state=StartSG.settings_tag
    ),

    Window(
        Format("Вы просмотрели все посты в выбранных категориях. Сбросьте настройки"),
        Row(
            SwitchTo(Const('Назад'), id='back', state=StartSG.start),
            Button(Const("Сбросить"), id="reset_settings",
                   on_click=clean_list_of_read_posts)
        ),
        state=StartSG.settings_reset
    ),
    getter=get_data
)
