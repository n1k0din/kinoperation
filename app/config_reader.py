import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    kino_api: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            kino_api=tg_bot["kino_api"]
        )
    )
