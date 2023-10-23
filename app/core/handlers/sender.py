from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
from sqlalchemy import select
from app.core.database.users import UserModel
from app.core.handlers.senderlist import SenderList
from app.core.utils.sender_state import StepsAdminForm
from app.core.utils.newletters import NewsletterManager
from app.core.keyboards.reply import get_cat_reply, get_main_reply, get_reply_confirm, get_reply_courses, get_reply_spclub
from app.core.keyboards.inline import confirm_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery

from app.core.database.database import Database
from app.config import load_config
config = load_config()


async def get_sender(message: Message, state: FSMContext):
    if message.text == 'Рассчитать стоимости':
        await message.answer(f'Для какого листа считаем?\r\nРасчитаем для него столбец "arrears".\r\nНазвание листа:')
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
        await state.update_data(options=message.text)
    elif message.text == 'Разослать стоимости':
        await message.answer(f'Разослано будет только лишь для тех, кто есть в листе.\nНапиши название листа по которому рассылаем.')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
    elif message.text == 'Разослать подтверждение курса/клуба':   
        await message.answer(f'Сообщение будет разослано по всей базе юзеров.\nВведите название листа, куда пишем тех, кто подтвердит:')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_SHEET_NAME)
    else: 
        await message.answer(f'Сообщение будет разослано по всей базе юзеров.\nВведите название рассылки:')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_NAME_CAMP)



async def get_sheet_name(message: Message, state: FSMContext, sender_list: SenderList, session: AsyncSession):
    await message.answer(f'Название листа: {message.text}\r\n')
    data = await state.get_data()
    if data.get('options')=='Разослать стоимости':      # рассылка стоимостей
        await message.answer(f'Надеюсь они уже рассчитаны.\r\nНапишите сообщение которое будет прикреплено.\nК вашему сообщению в конце будет добавлена строка "К оплате: 000р."')
        await state.update_data(sheet_name=message.text)
        await state.set_state(StepsAdminForm.GET_MESSAGE)
    elif data.get('options')=='Разослать подтверждение курса/клуба': # подтвержидение 
        await message.answer(f'Название листа: {message.text}\r\n Напишите сообщение рассылки:')
        await state.update_data(sheet_name=message.text)
        await state.set_state(StepsAdminForm.GET_MESSAGE)
    else:    # если расчет стоимостей  
        await state.clear() 
        await sender_list.calculation(message.text, session)



async def get_name_camp(message: Message, state: FSMContext):
    await message.answer(f'Имя компании: {message.text}\r\nНапишите сообщение для рассылки')
    await state.update_data(name_camp=message.text)
    await state.set_state(StepsAdminForm.GET_MESSAGE)


async def get_message(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if data.get('options')=='Разослать стоимости':
        await state.update_data(text=message.text)
        await message.answer(f'{message.text}\nК оплате: 000р.', reply_markup=confirm_keyboard)

    else:    
        await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)  
        data = await state.get_data()
        message_id = int(data.get('message_id'))
        chat_id = int(data.get('chat_id'))
        await confirm(message, message_id, chat_id, bot)


async def confirm(message: Message, message_id: int, chat_id: int, bot: Bot):
    await bot.copy_message(chat_id, chat_id, message_id)
    await message.answer(f'Вот это рассылка, все верно?', 
                        reply_markup=confirm_keyboard)


async def sender_decide(call: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession, sender_list: SenderList):
    if call.data == 'confirm_sender':
        data = await state.get_data()
        await call.message.edit_text('Начал рассылку', reply_markup=None)
       
        if data.get('options')=='Разослать стоимости':
            count = await sender_list.send_sum(data.get('sheet_name'), data.get('text'), data.get('options'))
            await bot.send_message(config.bot.ADMIN_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
            await bot.send_message(config.bot.DEV_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
        else:
            query = select(UserModel.tg_id) 
            answer = await session.execute(query)
            users_ids = [i[0] for i in answer]
            print(len(users_ids))
            count = await sender_list.broadcaster(message_id=int(data.get('message_id')), from_chat_id=int(data.get('chat_id')), name_camp=data.get('name_camp'), options=data.get('options'), users_ids=users_ids)          
            await bot.send_message(config.bot.ADMIN_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
            await bot.send_message(config.bot.DEV_ID, text=f'Рассылка окончена\nРазослано сообщений:  {count}')
    
    elif call.data == 'cancel_sender':
        await call.message.edit_text('Отменил рассылку', reply_markup=None)   

    await state.clear()     


#     k_b.button(text='Отправить простое сообщение всем')
#     k_b.button(text='Разослать подтверждение курса/клуба')
#     k_b.button(text='Рассчитать стоимости')
#     k_b.button(text='Разослать стоимости')