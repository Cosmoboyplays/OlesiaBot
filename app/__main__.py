from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from app.config import load_config
from app.core.database.database import Database
from app.core.handlers.basic import get_start, get_free_text, get_cat, send_in_all_chat
from app.core.middleware.dbmiddleware import DBSessionMiddleware
from app.core.utils.commands import set_commands
from app.core.handlers import reg_for_course, sender
from app.core.utils.reg_state import StepsForm
from app.core.utils.sender_state import StepsAdminForm
from app.core.handlers.senderlist import SenderList

import asyncio
import logging
import re

from app.core.middleware.countermiddleware import CounterMiddleware


config = load_config()
db = Database(config.db)


async def start_bot(bot: Bot):
    await db.init()
    await set_commands(bot)
    await bot.send_message(config.bot.DEV_ID, text='Уважаемый админ, бот запущен')


async def stop_bot(bot: Bot):
    await db.close()
    await bot.send_message(config.bot.DEV_ID, text='Уважаемый админ, бот остановлен')

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=config.bot.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.message.middleware.register(CounterMiddleware())
    dp.update.middleware.register(DBSessionMiddleware(db.session))
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # dp.message.register(get_inline, Command(commands='inline') )
    # dp.callback_query.register(select_course, F.data.startswith('Информация'))
    dp.message.register(get_start, Command(commands=['start', 'run']))
    # регистрация
    dp.message.register(reg_for_course.reg_for_course, F.text == 'Подтвердить выбор курса')
    dp.message.register(reg_for_course.get_name, StepsForm.GET_NAME)
    dp.message.register(reg_for_course.get_course, StepsForm.GET_COURSE)
    dp.message.register(reg_for_course.get_spclub, StepsForm.GET_SPCLUB)
    dp.message.register(reg_for_course.get_confirm, StepsForm.GET_CONFIRM)
    # рассылка
    dp.message.register(sender.get_sender, StepsAdminForm.GET_SENDER,
                        F.chat.id.in_({config.bot.DEV_ID, config.bot.ADMIN_ID})) ### почему так????\
    dp.message.register(sender.get_name_camp, StepsAdminForm.GET_NAME_CAMP,
                        F.chat.id.in_({config.bot.DEV_ID, config.bot.ADMIN_ID}))
    dp.message.register(sender.get_message, StepsAdminForm.GET_MESSAGE,
                        F.chat.id.in_({config.bot.DEV_ID, config.bot.ADMIN_ID}))
    dp.message.register(sender.get_sheet_name, StepsAdminForm.GET_SHEET_NAME,
                        F.chat.id.in_({config.bot.DEV_ID, config.bot.ADMIN_ID}))
    
    dp.callback_query.register(sender.sender_decide, F.data.in_(['confirm_sender', 'cancel_sender']))
    # dp.message.register(sender.get_confirm, StepsAdminForm.GET_CONFIRM,
    #                     F.chat.id.in_({config.bot.DEV_ID, config.bot.ADMIN_ID}))
    

    dp.message.register(get_cat, F.text == 'Отправь кота')
    dp.message.register(get_free_text, F.text) # соответствует любому тексту отправленном пользователем

    # dp.message.register(get_another_keyboard, F.text == 'Покажи другую интересную клавиатуру')
    # dp.message.register(get_photo, F.photo)
    
    # dp.message.register(get_keyboard, F.text=='Покажи интересную клавиатуру')
    # тут можно и регулярки использовать
    # dp.message.register(get_hello, F.text.lower().in_({'здрасте','привет'}))
    # dp.message.register(get_location, F.location)
    # dp.message.register(get_contact, F.contact)
    sender_lis = SenderList(bot)
    try:
        await dp.start_polling(bot, sender_list=sender_lis)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
