from dataclasses import dataclass
import os
from environs import Env


@dataclass
class TelegramBot:
    token: str
    api_token: str
    api_address: str
    admins: list[int]
    redis: str|None
    user_api: str
    pass_api: str
    # postgre_url: str|None


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    return TelegramBot(
        token=env.str("BOT_TOKEN"),
        api_token=env.str("API_TOKEN"),
        api_address=env.str("API_ADDRESS"),
        admins=list(map(int, env.list("ADMINS"))),
        redis = env.str("REDIS_URL", None),
        user_api = env.str("USER_API"),
        pass_api = env.str("PASS_API"),
        # postgre_url= env.str("POSTGRE_URL")
    )

config = load_config('.env')