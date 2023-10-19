from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
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
        await message.answer(f'Надеюсь они уже рассчитаны.\r\nНапишите сообщение которое будет прикреплено.\nК вашему сообщению в конце будет добавлена строка "К оплате: 000р."')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_MESSAGE)

    else: 
        await message.answer(f'Введите название рассылки:')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_NAME_CAMP)


async def get_sheet_name(message: Message, state: FSMContext, sender_list: SenderList):
    await message.answer(f'Название листа: {message.text}\r\n')
    await state.clear() 
    await sender_list.calculation(message.text, Bot)


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
            sender_list.send_sum(data.get('text') ,data.get('options'))
        else:
            count = await sender_list.broadcaster(int(data.get('message_id')), int(data.get('chat_id')), data.get('name_camp'), data.get('options'), session)
            await bot.send_message(config.bot.DEV_ID, text='Рассылка окончена\nРазослал {count} сообщений.')
            
    elif call.data == 'cancel_sender':
        await call.message.edit_text('Отменил рассылку', reply_markup=None)   

    await state.clear()     


#     k_b.button(text='Отправить простое сообщение всем')
#     k_b.button(text='Разослать подтверждение курса/клуба')
#     k_b.button(text='Рассчитать стоимости')
#     k_b.button(text='Разослать стоимости')