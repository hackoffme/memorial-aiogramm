from typing import Dict
import requests
from requests.auth import HTTPBasicAuth
import json
from tbot.config import config
from tbot import models

API_ADDRESS = config.api_address
API_TOKEN = config.api_token
USER_API = config.user_api
PASS_API = config.pass_api


def get_hi() -> str | None:
    q = requests.get(f'{config.api_address}/api/v1/settings',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    q = json.loads(q.text)
    for item in q:
        if item.get('name') == 'hi':
            return item.get('value', 'Привет')


def read_area():
    # api/v1/settings/areas/
    q = requests.get(f'{config.api_address}/api/v1/settings/areas/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    q = json.loads(q.text)
    return q


def read_tag():
    # api/v1/settings/tags/
    q = requests.get(f'{config.api_address}/api/v1/settings/tags/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    q = json.loads(q.text)
    return q


def create_user(tg_id: int):  # , tag_settings=, area_settings):
    # api/v1/tg_users/
    # m = {'tg_id': tg_id, 'tag_settings': tag_settings,
    #      'area_settings': area_settings}
    q = requests.post(
        f'{config.api_address}/api/v1/tg_users/', json={'tg_id': tg_id}, 
        auth=HTTPBasicAuth(USER_API, PASS_API))
    return q


def update_user(tg_id: int, **kwargs):
    # api/v1/tg_users/ID
    allowed_keys = ['tag_settings', 'area_settings', 'viewed_posts']
    pd = {k: kwargs.get(k) for k in allowed_keys if not kwargs.get(k) is None}
    q = requests.patch(
        f'{config.api_address}/api/v1/tg_users/{tg_id}/', 
        json=pd, 
        auth=HTTPBasicAuth(USER_API, PASS_API))
    return q.status_code


def read_user(tg_id: int) -> Dict:
    # api/v1/tg_users/ID/
    q = requests.get(f'{config.api_address}/api/v1/tg_users/{tg_id}/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = json.loads(q.text)
    ret.update({'status': q.status_code})
    return ret


def read_random_post(tg_id: int):
    # /api/v1/post/ID/
    q = requests.get(f'{config.api_address}/api/v1/post/{tg_id}/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = json.loads(q.text)
    ret.update({'status': q.status_code})
    return ret


def read_post_by_coordinates(tg_id: int, lat: float, lon: float):
    # /api/v1/post/1/get_post_by_coordinages/
    q = requests.get(f'{config.api_address}/api/v1/post/{tg_id}/get_post_by_coordinates/',
                     json={'lat': lat, 'lon': lon},
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = json.loads(q.text)
    ret.update({'status': q.status_code})
    return ret


def read_post_by_saved_coordinates(tg_id: int):
    q = requests.get(f'{config.api_address}/api/v1/post/{tg_id}/get_post_by_saved_coordinates/',
                     auth=HTTPBasicAuth(USER_API, PASS_API))
    ret = json.loads(q.text)
    ret.update({'status': q.status_code})
    return ret
