from aiogram import types

from tbot.repositories.repositories_api import vote
from tbot import models

def like_answer(vote: models.Vote)->str:
    match vote.status:
        case 422:
            return 'Ошибка голосования' 
        case 208:
            return f'👍 {vote.count_up} 👎🏾{vote.count_down} † Вы уже голосовали'
        case 201:
            return f'👍 {vote.count_up} 👎🏾{vote.count_down} † Ваш голос учтен'
        case 205:
            return f'👍 {vote.count_up} 👎🏾{vote.count_down} † Ваш голос отменен'


async def vote_up_handler(query: types.CallbackQuery, callback_data: dict):
    ret = vote(query.from_user.id, callback_data['post_id'] , True)
    await query.answer(like_answer(ret))
    
    
async def vote_down_handler(query: types.CallbackQuery, callback_data: dict):
    ret = vote(query.from_user.id, callback_data['post_id'] , False)
    await query.answer(like_answer(ret))
    