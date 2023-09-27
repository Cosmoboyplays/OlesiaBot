# pip3 install environs

from environs import Env
from dataclasses import dataclass
from ..config import BotConfig


@dataclass
class Bots:
    bot_token: str
    admin_id: int

@dataclass
class Settings:
    bots: Bots


def get_settings(config: BotConfig):
    env = Env()
    # env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str(config.TOKEN), 
            admin_id=env.int(config.DEV_ID)
        )
    )        

settings = get_settings(BotConfig)

""" В целом, данный код используется для загрузки настроек из файла .env
и создания объекта класса Settings, который содержит эти настройки. 
Загрузка настроек из файла .env полезна, когда вам нужно настроить 
приложение или библиотеку таким образом, чтобы определенные параметры 
были гибкими и могли изменяться без изменения самого кода. 
Это удобно при разработке и развертывании программного обеспечения.
"""
