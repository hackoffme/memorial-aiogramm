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
    webhook_host: str|None
    webhook_path: str|None
    webapp_host: str|None
    webapp_port: int|None


def load_config(path: str = None)->TelegramBot:
    env = Env()
    env.read_env(path)
    return TelegramBot(
        token=env.str("BOT_TOKEN"),
        api_address=env.str("API_ADDRESS"),
        redis = env.str("REDIS_URL", None),
        user_api = env.str("USER_API"),
        pass_api = env.str("PASS_API"),
        webhook_host=env.str("WEBHOOK_HOST", None),
        webhook_path=env.str("WEBHOOK_PATH", None),
        webapp_host=env.str("WEBAPP_HOST", None),
        webapp_port=env.int("WEBAPP_PORT", None)
    )

config = load_config('.env')