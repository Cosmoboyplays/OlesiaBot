from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
from app.core.handlers.senderlist import SenderList
from app.core.utils.sender_state import StepsAdminForm
from app.core.utils.newletters import NewsletterManager
from app.core.keyboards.reply import get_cat_reply, get_main_reply, get_reply_confirm, get_reply_courses, get_reply_spclub
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery

from app.core.database.database import Database
from app.config import load_config
config = load_config()


async def get_sender(message: Message, state: FSMContext):
    if message.text == 'Рассчитать стоимости':
        pass
 
    else: 
        await message.answer(f'Введите название рассылки:')
        await state.update_data(options=message.text)
        await state.set_state(StepsAdminForm.GET_NAME_CAMP)


async def get_name_camp(message: Message, state: FSMContext):
    await message.answer(f'Имя компании: {message.text}\r\nНапишите сообщение для рассылки')
    await state.update_data(name_camp=message.text)
    await state.set_state(StepsAdminForm.GET_MESSAGE)


async def get_message(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    
    data = await state.get_data()
    message_id = int(data.get('message_id'))
    chat_id = int(data.get('chat_id'))
    await confirm(message, message_id, chat_id, bot)


async def confirm(message: Message, message_id: int, chat_id: int, bot: Bot):
    await bot.copy_message(chat_id, chat_id, message_id)

    await message.answer(f'Вот это рассылка, все верно?', 
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=
                        [
                             [
                                 InlineKeyboardButton(
                                     text='Подтвердить',
                                     callback_data='confirm_sender'
                                 )
                             ],
                             [
                                 InlineKeyboardButton(
                                     text='Отменить',
                                     callback_data='cancel_sender'
                                 )
                             ]
                        ]
                        ))

async def sender_decide(call: CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession, sender_list: SenderList):
    data = await state.get_data()
    message_id = int(data.get('message_id'))
    chat_id = int(data.get('chat_id'))
    name_camp = data.get('name_camp')
    options= data.get('options')
    
    if call.data == 'confirm_sender':
        await call.message.edit_text('Начал рассылку', reply_markup=None)
        count = await sender_list.broadcaster(message_id, chat_id, name_camp, options)

        # тут рассылка
            
    elif call.data == 'cancel_sender':
        await call.message.edit_text('Отменил рассылку', reply_markup=None)   

    await state.clear()     


#     k_b.button(text='Отправить простое сообщение всем')
#     k_b.button(text='Разослать подтверждение курса/клуба')
#     k_b.button(text='Рассчитать стоимости')
#     k_b.button(text='Разослать стоимости')