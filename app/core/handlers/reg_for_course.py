from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.utils.reg_state import StepsForm
from app.core.keyboards.reply import get_cat_reply, get_main_reply, get_reply_confirm, get_reply_courses, get_reply_spclub
from app.core.database.users import UserModel
from app.core.utils.google_api import GoogleTable
from app.config import load_config

config = load_config()

async def reg_for_course(message: Message, state: FSMContext, session: AsyncSession):
    result = await session.execute(select(UserModel).filter_by(tg_id=message.from_user.id))
    user = result.scalar_one_or_none()
    if user.course == None:
        await message.answer(f'{message.from_user.first_name}, начинаем регистрацию на курс! Введите имя и фамилию:',
                             reply_markup=None)
        await state.update_data(status='New')      # если человек первый раз подтверждает то запишем его в лист 'Новые'
        await state.set_state(StepsForm.GET_NAME)
    else:
        await message.answer(
            f'Вы с нами не первый месяц! Если данные не изменились и вы хотите продолжить занятия, пожалуйста подтвердите')
        await state.update_data(full_name=user.full_name, course=user.course, sp_club=user.sp_club, status='Old')
        await state.set_state(StepsForm.GET_CONFIRM)
        await message.answer(f'Вас зовут: {user.full_name}\r\n' \
                                  f'Ваш курс: {user.course}\r\n' \
                                  f'Ваш клуб: {user.sp_club}', reply_markup=get_reply_confirm())


async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Вас зовут {message.text}\nВыберите курс',
                        reply_markup=get_reply_courses())
    await state.update_data(full_name=message.text)
    await state.set_state(StepsForm.GET_COURSE)


async def get_course(message: Message, state: FSMContext, bot: Bot):
    if message.text=='Я не знаю':
        await message.answer(f'C вами свяжется Олеся', reply_markup=get_main_reply())
        await bot.send_message(config.bot.ADMIN_ID, f'Свяжись с @{message.from_user.username}, человек не знает курс')
        await state.clear()
    
    elif message.text=='Я только в разговорный клуб':
        await message.answer(f'Вы без курса\r\n' \
                            f'Выберете разговорный клуб',
                            reply_markup=get_reply_spclub())
        await state.set_state(StepsForm.GET_SPCLUB)

    elif message.text not in ('"C нуля" ENG - пятница 18:00',
                                '"А1" ENG воскресенье 13:00',
                                '"А1-А2" ENG вторник 18:00',
                                '"А2" ENG среда 18:30',
                                '"В1+" ENG вторник 18:00',
                                '"В2" ENG четверг 18:30'):
        await message.answer(f'Пожалуйста в следующий раз выбирайте с клавиатуры :)', reply_markup=get_main_reply())
        await state.clear()
   
    else:    
        await message.answer(f'Ваш курс: {message.text}\r\n' \
                            f'Выберете разговорный клуб',
                            reply_markup=get_reply_spclub())
        await state.update_data(course=message.text)
        await state.set_state(StepsForm.GET_SPCLUB)


async def get_spclub(message: Message, state: FSMContext, bot: Bot):
    if message.text=='Мне не нужен разговорный клуб':
        await state.update_data(sp_club='нет')

    elif message.text=='Я не знаю':
        await message.answer(f'C вами свяжется Олеся', reply_markup=get_main_reply())
        await bot.send_message(config.bot.ADMIN_ID, f'Свяжись с @{message.from_user.username}, человек не знает в какой разговорный клуб')    
        return await state.clear()

    elif message.text not in ('SC 1 "А1-А2" ENG пятница 18:30',
                              'SC 2 "В1-В2" ENG пятница 18:30',
                              'SC 3 "С1" ENG понедельник 18:00'):
        await message.answer(f'Пожалуйста в следующий раз выбирайте с клавиатуры :)', reply_markup=get_main_reply())
        await state.clear()

    else:
        await state.update_data(sp_club=message.text)

    data = await state.get_data()   
    await message.answer(f'Вас зовут: {data["full_name"]}\r\n' \
                         f'Ваш курс: {data.get("course", "нет")}\r\n' \
                         f'Ваш клуб: {data["sp_club"]}')
    await state.set_state(StepsForm.GET_CONFIRM)
    await message.answer(f'Вы подтверждаете введенные данные?', reply_markup=get_reply_confirm())


async def get_confirm(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    if message.text == 'Нет' and data['status'] == 'New':
        await state.clear()
        await message.answer('Данные не подтверждены :(', reply_markup=get_main_reply())

    elif message.text == 'Нет' and data['status'] == 'Old':
        await state.clear()
        await state.update_data(status='Old')
        await state.set_state(StepsForm.GET_NAME)
        await message.answer('Данные не подтверждены, придется заполнить заново\n Введите имя и фамилию:')

    elif message.text == 'Да':
        await state.clear()
        result = await session.execute(select(UserModel).filter_by(tg_id=message.from_user.id))
        user = result.scalar_one_or_none()
        try:
            if user:
                user.full_name = data['full_name']
                user.course = data.get("course", "нет")
                user.sp_club = data["sp_club"]
                user.arrears = 0
            await session.commit()

            s = [[message.from_user.id, message.from_user.username, data['full_name'], data.get("course", "нет"),
                  data["sp_club"], 0]]
            gt = GoogleTable()                                                                # записываем GoogleSheets
            if data['status'] == 'Old':
                gt.append_user(s)
            else:
                gt.append_user(s, 'Новые')

            await message.answer(
                'Спасибо! Данные подтверждены :)\r\nРасчет оплаты придет чуть позже.\r\nМогу отправить кота ;)',
                reply_markup=get_cat_reply())
        except:
            await message.answer('Данные не отправлены!Начните с начала', reply_markup=get_main_reply())
    else:
        await message.answer('Вы данные подтверждаете?', reply_markup=get_reply_confirm())