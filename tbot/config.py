from dataclasses import dataclass
import os
from environs import Env


@dataclass
class TelegramBot:
    token: str
    api_token: str
    api_address: str
    admins: list[int]


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    return TelegramBot(
        token=env.str("BOT_TOKEN"),
        api_token=env.str("API_TOKEN"),
        api_address=env.str("API_ADDRESS"),
        admins=list(map(int, env.list("ADMINS")))
    )

config = load_config('.env')