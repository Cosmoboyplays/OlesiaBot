from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.core.utils.sender_state import StepsForm
from app.core.keyboards.reply import get_cat_reply, get_main_reply, get_reply_confirm, get_reply_courses, get_reply_spclub
from app.config import load_config
config = load_config()


async def get_sender(message: Message, state: FSMContext):
    if message.text in ('Отправить простое сообщение всем', 'Разослать подтверждение курса/клуба'):
        await message.answer(f'Введите название рассылки:')
        await state.set_state(StepsForm.GET_NAME_CAMP)

    elif     




    
#     k_b.button(text='Отправить простое сообщение всем')
#     k_b.button(text='Разослать подтверждение курса/клуба')
#     k_b.button(text='Рассчитать стоимости')
#     k_b.button(text='Разослать стоимости')