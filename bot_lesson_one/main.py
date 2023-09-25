# pip3 install aiogram

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

from core.handlers.basic import get_start, get_photo, get_hello, get_contact, get_keyboard, get_location, get_another_keyboard, get_free_text
from core.handlers.basic import get_inline
from core.settings import settings
from core.utils.commands import set_commands
from core.handlers.callback import select_course 

import asyncio
import logging
import re

from core.middleware.countermiddleware import CounterMiddleware
 

async def start_bot(bot: Bot):
    await set_commands(bot) # так делается меню
    await bot.send_message(settings.bots.admin_id, text='Уважаемый админ, бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Уважаемый админ, бот остановлен')    



async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    dp = Dispatcher()
    dp.message.middleware.register(CounterMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot) 
    dp.message.register(get_inline, Command(commands='inline') )
    dp.callback_query.register(select_course, F.data.startswith('Информация'))
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(get_keyboard, F.text=='Покажи интересную клавиатуру')
    dp.message.register(get_another_keyboard, F.text=='Покажи другую интересную клавиатуру')
    dp.message.register(get_photo, F.photo)                                                  # регистрируем хэндлер, который фото сохраняет(в 3 версии черз F делается)
    dp.message.register(get_hello, F.text.lower().in_({'здрасте','привет'}))                 # тут можно и регулярки использовать
    dp.message.register(get_location, F.location)
    dp.message.register(get_contact, F.contact)
    dp.message.register(get_free_text, lambda message: re.fullmatch(r'.+', message.text))    # соответсвует любому тексту отправленном пользователем 
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()    



if __name__ == '__main__':
    asyncio.run(start())



    