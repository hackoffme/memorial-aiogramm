from dataclasses import dataclass
import os
from environs import Env


@dataclass
class TelegramBot:
    token: str
    api_address: str
    redis: str|None
    user_api: str
    pass_api: str
    webhook_host: str
    webhook_path: str
    webapp_host: str
    webapp_port: int
    # postgre_url: str|None


def load_config(path: str = None)->TelegramBot:
    env = Env()
    env.read_env(path)
    return TelegramBot(
        token=env.str("BOT_TOKEN"),
        api_address=env.str("API_ADDRESS"),
        redis = env.str("REDIS_URL", None),
        user_api = env.str("USER_API"),
        pass_api = env.str("PASS_API"),
        webhook_host=env.str("WEBHOOK_HOST"),
        webhook_path=env.str("WEBHOOK_PATH"),
        webapp_host=env.str("WEBAPP_HOST"),
        webapp_port=env.int("WEBAPP_PORT")
    )

config = load_config('.env')