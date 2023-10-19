from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class BotConfig:
    BOT_TOKEN: str
    DEV_ID: int
    ADMIN_ID: int


@dataclass
class DatabaseConfig:
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASS: str


@dataclass
class Config:
    bot: BotConfig
    db: DatabaseConfig


def load_config() -> Config:
    env = Env()
    env.read_env(".env")

    return Config(
        bot=BotConfig(
            BOT_TOKEN=env.str("BOT_TOKEN"),
            DEV_ID=env.int("DEV_ID"),
            ADMIN_ID=env.int("ADMIN_ID")
        ),
        db=DatabaseConfig(
            HOST=env.str("DB_HOST"),
            PORT=env.int("DB_PORT"),
            NAME=env.str("DB_NAME"),
            USER=env.str("DB_USER"),
            PASS=env.str("DB_PASS"),
        )
    )
