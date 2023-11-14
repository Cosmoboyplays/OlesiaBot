from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from app.core.database.users import UserModel
from app.core.handlers.senderlist import SenderList
from app.core.keyboards.reply import get_reply_confirm
from app.core.utils.newletters import NewsletterManager
from app.core.utils.sender_state import StepsAdminForm
from app.core.utils.google_api import GoogleTable
from app.core.keyboards.inline import confirm_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery

from app.core.database.database import Database
from app.config import load_config
from app.core.utils.text import TextButton

config = load_config()


async def get_sender(message: Message, state: FSMContext):
    if message.text == TextButton.count_price:
        await message.answer(f'Для какого листа считаем?\r\nРасчитаем для него столбец "arrears". Добавим 10р.'
                             f'\r\nНазвание листа:')
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
        await state.update_data(options=message.text)
    elif message.text == TextButton.send_price:
        await message.answer(f'Разослано будет только лишь для тех, кто есть в листе.\n'
                             f'Напиши название листа по которому рассылаем.')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
    elif message.text == TextButton.send_confirm:
        await message.answer(f'Сообщение будет разослано по всей базе юзеров.\nВведите название листа, куда пишем тех, '
                             f'кто подтвердит:')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
    elif message.text == TextButton.send_by_sheet:
        await message.answer(f'Сообщение будет разослано по листу.\nВведите название листа, по которому рассылаем')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
    else:
        await message.answer(f'Сообщение будет разослано по всей базе юзеров.\nВведите название рассылки:')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_NAME_CAMP)


async def get_sheet_name(message: Message, state: FSMContext, sender_list: SenderList, session: AsyncSession):
    gt = GoogleTable()
    if gt.check_sheet(message.text):
        pass
    else:
        await message.answer(f'Нет такого листа в таблице!Заново!')
        await state.clear()
        return

    await message.answer(f'Название листа: {message.text}\r\n')
    data = await state.get_data()
    if data.get('options') == TextButton.send_price:  # рассылка стоимостей
        await message.answer(f'Надеюсь они уже рассчитаны.\r\nНапишите сообщение которое будет прикреплено.'
                             f'\nК вашему сообщению в конце будет добавлена строка "К оплате: 000р."')
        await state.update_data(sheet_name=message.text)
        await state.set_state(StepsAdminForm.GET_MESSAGE)

    elif data.get('options') == TextButton.send_by_sheet:
        await message.answer(f'Напишите сообщение которое будет прикреплено к вашей рассылке по листу.')
        await state.update_data(sheet_name=message.text)
        await state.set_state(StepsAdminForm.GET_MESSAGE)

    elif data.get('options') == TextButton.send_confirm:  # подтверждение
        newsletter_manager = NewsletterManager()
        newsletter_manager.update_list_name(message.text)
        await message.answer(f'Напишите сообщение рассылки:')
        await state.set_state(StepsAdminForm.GET_MESSAGE)

    else:  # расчет стоимостей
        await state.clear()
        await sender_list.calculation(message.text, session)


async def get_name_camp(message: Message, state: FSMContext):
    await message.answer(f'Имя компании: {message.text}\r\nНапишите сообщение для рассылки')
    await state.update_data(name_camp=message.text)
    await state.set_state(StepsAdminForm.GET_MESSAGE)


async def get_message(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data.get('options') == TextButton.send_price:
        await state.update_data(text=message.text)
        await message.answer(f'{message.text}\nК оплате: 000р.', reply_markup=confirm_keyboard)

    elif data.get('options') == TextButton.send_by_sheet:
        await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
        await message.answer(f'Добавить ли клавиатуру подтверждения клуба/курса?', reply_markup=get_reply_confirm())
        await state.set_state(StepsAdminForm.GET_REPLY_KEY)

    else:
        await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
        data = await state.get_data()
        message_id = int(data.get('message_id'))
        chat_id = int(data.get('chat_id'))
        await confirm(message, message_id, chat_id, bot)


async def get_confirm_key(message: Message, bot: Bot, state: FSMContext):
    if message.text == 'Да':
        await state.update_data(key_confirm=1)
    else:
        await state.update_data(key_confirm=None)

    data = await state.get_data()
    message_id = int(data.get('message_id'))
    chat_id = int(data.get('chat_id'))

    await confirm(message, message_id, chat_id, bot)


async def confirm(message: Message, message_id: int, chat_id: int, bot: Bot):
    await bot.copy_message(chat_id, chat_id, message_id)
    await message.answer(f'Вот это рассылка, все верно?',
                         reply_markup=confirm_keyboard)


async def sender_decide(call: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession,
                        sender_list: SenderList):

    if call.data == 'confirm_sender':
        data = await state.get_data()
        await call.message.edit_text('Начал рассылку', reply_markup=None)

        if data.get('options') in (TextButton.send_price, TextButton.send_by_sheet):
            count = await sender_list.send_by_sheet(data)
            await bot.send_message(config.bot.ADMIN_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
            await bot.send_message(config.bot.DEV_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
        else:
            query = select(UserModel.tg_id).where(UserModel.state == 'member')
            answer = await session.execute(query)
            users_ids = [i[0] for i in answer]
            count = await sender_list.broadcaster(data, users_ids=users_ids)
            await bot.send_message(config.bot.ADMIN_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
            await bot.send_message(config.bot.DEV_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')

    elif call.data == 'cancel_sender':
        await call.message.edit_text('Отменил рассылку', reply_markup=None)

    await state.clear()


