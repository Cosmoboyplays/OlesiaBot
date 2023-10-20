from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.core.utils.reg_state import StepsForm
from app.core.keyboards.reply import get_cat_reply, get_main_reply, get_reply_confirm, get_reply_courses, get_reply_spclub
from app.config import load_config
config = load_config()

from app.core.database.users import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert



async def get_pay(message: Message, state: FSMContext):
    await message.answer(f'Получаю фотку или файл или текст в ответ на сумму.',
                         reply_markup=None)
    