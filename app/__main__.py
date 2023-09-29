from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from app.config import load_config
from app.core.database.database import Database
from app.core.handlers.basic import get_start, get_photo, get_another_keyboard, get_free_text, get_inline
from app.core.handlers.basic import save_in_db
from app.core.middleware.config import ConfigMiddleware
from app.core.middleware.database import DBSessionMiddleware
from app.core.utils.commands import set_commands
from app.core.handlers.callback import select_course

import asyncio
import logging
import re

from app.core.middleware.countermiddleware import CounterMiddleware
from app.texts import Text

config = load_config()
db = Database(config.db)


async def start_bot(bot: Bot):
    await db.init()

    await set_commands(bot)
    await bot.send_message(config.bot.DEV_ID, text=Text.ON_STARTUP)


async def stop_bot(bot: Bot):
    await db.close()
    await bot.send_message(config.bot.DEV_ID, text=Text.ON_SHUTDOWN)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=config.bot.BOT_TOKEN, parse_mode='HTML')

    dp = Dispatcher()
    dp.message.middleware.register(CounterMiddleware())
    dp.update.middleware.register(DBSessionMiddleware(db.session))
    dp.update.middleware.register(ConfigMiddleware(config))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_inline, Command(commands='inline') )
    dp.callback_query.register(select_course, F.data.startswith('Информация'))

    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(get_another_keyboard, F.text == 'Покажи другую интересную клавиатуру')
    dp.message.register(get_photo, F.photo)
    dp.message.register(save_in_db, F.text == 'Сохрани контакт')

    # соответсвует любому тексту отправленном пользователем
    dp.message.register(get_free_text, lambda message: re.fullmatch(r'.+',
                                                                    message.text))
    # dp.message.register(get_keyboard, F.text=='Покажи интересную клавиатуру')
    # тут можно и регулярки использовать
    # dp.message.register(get_hello, F.text.lower().in_({'здрасте','привет'}))
    # dp.message.register(get_location, F.location)
    # dp.message.register(get_contact, F.contact)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
