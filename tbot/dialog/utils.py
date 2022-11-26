from aiogram.types import Message, InputFile, MediaGroup, InputMediaPhoto
from aiogram.utils.markdown import quote_html, html_decoration
from aiogram.utils.exceptions import BadRequest
from tbot import models
from tbot.keyboards.like import get_keyboard
async def send_post(m: Message, post: models.Posts):
    await m.answer(f'<u><b>{quote_html(post.title)} </b></u>\n {post.text}')
    if post.images_set:
        group = MediaGroup()
        for item in post.images_set:
            group.attach_photo(InputMediaPhoto(InputFile.from_url(item.image)))
        try:
            await m.answer_media_group(group)
        except BadRequest as err:
            print(err)

    await m.answer_location(longitude=post.lon, latitude=post.lat, reply_markup=get_keyboard(post.id))
    


