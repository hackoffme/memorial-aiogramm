from typing import List
from pydantic import parse_raw_as
import requests
from requests.auth import HTTPBasicAuth
import json
from tbot.config import config
from tbot import models

API_ADDRESS = config.api_address
USER_API = config.user_api
PASS_API = config.pass_api
HI = ''


def get_hi() -> str:
    if HI:
        return HI
    q = requests.get(f'{config.api_address}/api/v1/settings',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    q = json.loads(q.text)
    for item in q:
        if item.get('name', None) == 'hi':
            return item.get('value', 'Привет')
    return 'Привет дорогой друг'


def read_area() -> List[models.Area]:
    # api/v1/settings/areas/
    q = requests.get(f'{config.api_address}/api/v1/settings/areas/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = parse_raw_as(List[models.Area], q.text)
    return ret


def read_tag() -> List[models.Tag]:
    # api/v1/settings/tags/
    q = requests.get(f'{config.api_address}/api/v1/settings/tags/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = parse_raw_as(List[models.Tag], q.text)
    return ret


def create_user(tg_id: int) -> models.TgUser:
    # api/v1/tg_users/
    q = requests.post(
        f'{config.api_address}/api/v1/tg_users/', json={'tg_id': tg_id},
        auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = models.TgUser.parse_raw(q.text)
    ret.status = q.status_code
    return ret


def update_user(tg_id: int, **kwargs) -> models.TgUser:
    # api/v1/tg_users/ID
    allowed_keys = ['tag_settings', 'area_settings', 'viewed_posts']
    pd = {k: kwargs.get(k) for k in allowed_keys if not kwargs.get(k) is None}
    q = requests.patch(
        f'{config.api_address}/api/v1/tg_users/{tg_id}/',
        json=pd,
        auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = models.TgUser.parse_raw(q.text)
    ret.status = q.status_code
    return ret


def read_user(tg_id: int) ->models.TgUser:
    # api/v1/tg_users/ID/
    q = requests.get(f'{config.api_address}/api/v1/tg_users/{tg_id}/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = models.TgUser.parse_raw(q.text)
    ret.status = q.status_code
    return ret


def read_random_post(tg_id: int) -> models.Posts:
    # /api/v1/post/ID/
    q = requests.get(f'{config.api_address}/api/v1/post/{tg_id}/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = models.Posts.parse_raw(q.text)
    ret.status = q.status_code
    return ret


def read_post_by_coordinates(tg_id: int, lat: float, lon: float) -> models.Posts:
    # /api/v1/post/1/get_post_by_coordinages/
    q = requests.get(f'{config.api_address}/api/v1/post/{tg_id}/get_post_by_coordinates/',
                     json={'lat': lat, 'lon': lon},
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = models.Posts.parse_raw(q.text)
    ret.status = q.status_code
    return ret


def read_post_by_saved_coordinates(tg_id: int) -> models.Posts:
    # /api/v1/post/{tg_id}/get_post_by_saved_coordinates/'
    q = requests.get(f'{config.api_address}/api/v1/post/{tg_id}/get_post_by_saved_coordinates/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = models.Posts.parse_raw(q.text)
    ret.status = q.status_code
    return ret
