from aiogram.types import CallbackQuery
from aiogram import Bot

async def select_course(call: CallbackQuery, bot: Bot):
    model = call.data
    answer = f'{call.message.from_user.first_name}, выбран {model} '
    print(call.message.from_user)
    await call.message.answer(answer)
    await call.answer() # это ответ телеграмму, чтобы на кнопке не горели часики
