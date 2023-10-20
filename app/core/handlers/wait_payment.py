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


async def get_pay(message: Message, state: FSMContext, bot: Bot):   
    if message.document:
        await bot.forward_message(config.bot.ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.clear()
        await message.answer(f'Спасибо админ проверит, и если что свяжется с вами.\nХочешь кота?',
                            reply_markup=get_cat_reply())
    elif message.photo:
        await bot.forward_message(config.bot.ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.clear()
        await message.answer(f'Спасибо админ проверит, и если что свяжется с вами.\nХочешь кота?',
                            reply_markup=get_cat_reply())
    else:
        await message.answer(f'Я жду скрин! Или файл.',
                         reply_markup=None)    
        
    