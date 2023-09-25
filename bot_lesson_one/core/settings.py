# pip3 install environs

from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int

@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"), 
            admin_id=env.int("ADMIN_ID")
        )
    )        

settings = get_settings('bot_lesson_one/input')

""" В целом, данный код используется для загрузки настроек из файла .env
и создания объекта класса Settings, который содержит эти настройки. 
Загрузка настроек из файла .env полезна, когда вам нужно настроить 
приложение или библиотеку таким образом, чтобы определенные параметры 
были гибкими и могли изменяться без изменения самого кода. 
Это удобно при разработке и развертывании программного обеспечения.
"""
