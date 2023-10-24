from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.core.keyboards.reply import get_cat_reply
from app.core.database.users import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import load_config

config = load_config()


async def get_pay(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    if message.document or message.photo:
        await bot.forward_message(config.bot.ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        await state.clear()
        try:
            await UserModel.update_arrears(session, message.from_user.id, 0)
        except Exception as e:
            print(str(e))
        await message.answer(f'Спасибо, администратор проверит и, если что-то не так, свяжется с вами.\nХочешь кота?',
                                reply_markup=get_cat_reply())
    else:
        await message.answer(f'Я жду скрин! Или файл.',
                         reply_markup=None)
        
    