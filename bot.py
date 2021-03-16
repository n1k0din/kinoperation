import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.common import register_handlers_common
from app.handlers.quiz import register_handlers_quiz

logger = logging.getLogger(__name__)


async def set_commands(bot):
    commands = [
        BotCommand(command="/random", description="Случайный фильм"),
        BotCommand(command="/stop", description="Рыба-акула игра утонула"),
        ]

    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s -%(name)s - %(message)s"
    )
    logger.error("Starting bot")

    config = load_config("config/bot.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp, config.tg_bot.admin_id)
    register_handlers_quiz(dp)

    await set_commands(bot)

    await dp.start_polling()









if __name__ == '__main__':
    asyncio.run(main())
