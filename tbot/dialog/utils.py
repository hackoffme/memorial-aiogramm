from aiogram.types import Message
async def send_post(m: Message, post):
    await m.answer(post['title'])
    await m.answer(post['text'])
    await m.answer_location(longitude=post['lon'], latitude=post['lat'])