from aiogram.types import  ContentType

from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Group, Multiselect, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.input import MessageInput

from tbot.repositories import repositories_api
from tbot.dialog.state import StartSG
from tbot.dialog.stayinghome import stayinghome, clean_list_of_read_posts
from tbot.dialog.wilkingaround import walkingaround, walkingaround_show_more
from tbot.dialog.user_input import messange_input
from tbot.dialog.settings import get_settings, settings_end


async def get_data(*args, **kwargs):
    # Геттер для диалога
    area = repositories_api.read_area()
    tag = repositories_api.read_tag()
    return {'area_settings': area, 'tag_settings': tag}  # , 'hi': hi}


async def start_dialog(_, manager: DialogManager, **kwarg):
    hi = repositories_api.get_hi()
    await manager.event.answer(hi)
    id = manager.event.from_id
    user = repositories_api.read_user(id)
    if user.get('status') == 404:
        repositories_api.create_user(id)


dialog = Dialog(
    Window(
        Format("<b><i>Меню навигации</i></b>"),
        Row(
            Button(Const("🏠Сижу дома"), id="stayinghome",
                   on_click=stayinghome),
            Button(Const("🚶‍♂️Иду ногами"), id="walkingaround",
                   on_click=walkingaround),
            Button(Const("⚙️Настройки"), id="options",
                   on_click=get_settings),
        ),
        MessageInput(messange_input,  content_types=[
                     ContentType.LOCATION, ContentType.TEXT]),
        state=StartSG.start
    ),
    Window(
        Format("<b><i>Хотите больше, нажмите показать статью</i></b>"),
        Row(
            SwitchTo(Const('⬅️Назад'), id='back', state=StartSG.start),
            Button(Const('➡️Показать еще статью'),
                   id="im_lucky", on_click=stayinghome),
        ),
        MessageInput(messange_input,  content_types=[
            ContentType.LOCATION, ContentType.TEXT]),
        state=StartSG.stayinghome
    ),
    Window(
        Format("<b><i>Хотите больше, нажмите показать статью</i></b>"),
        Row(
            SwitchTo(Const('⬅️Назад'), id='back', state=StartSG.start),
            Button(Const('➡️Показать еще статью'),
                   id="", on_click=walkingaround_show_more),
        ),
        MessageInput(messange_input,  content_types=[
            ContentType.LOCATION, ContentType.TEXT]),
        state=StartSG.walkingaround
    ),
    Window(
        Format("<b><i>Привет! это мои настройки. Выберите район поиска:</i></b>"),
        Group(Multiselect(
            Jinja('✅ {{item["title"]}}'),
            Jinja('❌ {{item["title"]}}'),
            id="area_settings",
            item_id_getter=lambda x: x['slug'],
            items='area_settings'
        ),
            width=2
        ),
        SwitchTo(Const("Далее"), id="next_settings",
                 state=StartSG.settings_tag),
        MessageInput(messange_input,  content_types=[
            ContentType.LOCATION, ContentType.TEXT]),
        state=StartSG.settings_area
    ),
    Window(
        Format("<b><i>Выберите теги, которые вым интересны</i></b>"),
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
        MessageInput(messange_input,  content_types=[
            ContentType.LOCATION, ContentType.TEXT]),
        state=StartSG.settings_tag
    ),

    Window(
        Format(
            "<b><i>Вы просмотрели все посты в выбранных категориях. Сбросьте настройки</i></b>"),
        Row(
            SwitchTo(Const('⬅️Назад'), id='back', state=StartSG.start),
            Button(Const("🔃Сбросить"), id="reset_settings",
                   on_click=clean_list_of_read_posts)
        ),
        MessageInput(messange_input,  content_types=[
            ContentType.LOCATION, ContentType.TEXT]),
        state=StartSG.settings_reset
    ),
    getter=get_data,
    on_start=start_dialog

)
