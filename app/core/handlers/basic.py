import asyncio
from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import load_config

from app.config import Config
from app.core.database.users import UserModel
from app.core.keyboards.reply import get_admin_reply, get_cat_reply, get_main_reply
from app.core.keyboards.inline import  select_course
from datetime import datetime
from sqlalchemy import select, insert

import requests
import os

API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
config = load_config()

async def get_cat(message: Message, bot: Bot, session: AsyncSession):
    await bot.send_photo(message.chat.id, photo=requests.get(API_CATS_URL).json()[0]['url'])
    await asyncio.sleep(2)

    result = await session.execute(select(UserModel).filter_by(tg_id=message.from_user.id))
    user = result.scalar_one_or_none()
    if user.course == None:
        await message.answer(f'Хочешь записаться на курс по изучению иностранного языка или в разговорный клуб?',
                            reply_markup=get_main_reply())
    else:
        await message.answer(f'Хочешь кота?',
                            reply_markup=get_cat_reply())


    
async def get_start(message: Message, bot: Bot, counter: str, session: AsyncSession):
    if message.from_user.id==config.bot.DEV_ID:
         await message.answer(f'Ты здесь босс, что делаем?',
                         reply_markup=get_admin_reply())
       
    else:
        if not list(await session.execute(select(UserModel).filter_by(tg_id=message.from_user.id))):
            await session.execute(insert(UserModel).values(tg_id=message.from_user.id,
                                                            name=message.from_user.username
                                                          )
                                 )
        await session.commit()   
        await message.answer(f'Привет <b>{message.from_user.first_name}.</b>\nХочешь записаться на курс по изучению иностранного языка или в разговорный клуб?\r\nМогу просто отправить кота ;)',
                            reply_markup=get_main_reply())
    


    # await message.answer(f'Сообщение #{counter}')
    # await message.answer(f'Привет <b>{message.from_user.first_name}. </b>\nСкоро тут будет запись на курсы, мы оповестим тебя о ней.\nПока могу отправить кота :)',
    #                      reply_markup=get_reply_keyboard())  # просто ответ | второй аргумент это клава
    # await message.reply(f'Привет <b>{message.from_user.first_name}. </b>') # ответ с пересланным 

async def get_free_text(message: Message, bot: Bot, session: AsyncSession):
    await message.answer('Я не умею на такое отвечать :(')
    await asyncio.sleep(2)

    result = await session.execute(select(UserModel).filter_by(tg_id=message.from_user.id))
    user = result.scalar_one_or_none()
    if user.course == None:
        await message.answer(f'Хочешь записаться на курс по изучению иностранного языка или в разговорный клуб?',
                            reply_markup=get_main_reply())
    else:
        await message.answer(f'Хочешь кота?',
                            reply_markup=get_cat_reply())



async def send_in_all_chat(message: Message, bot: Bot, session: AsyncSession):
    count = 0
    # Извлечение всех строк из таблицы
    query = select(UserModel.id, UserModel.tg_id, UserModel.name)
    result = await session.execute(query)
    for row in result:
        await bot.send_message(row[1], 'Это рассылка из базы')
        count += 1
        await asyncio.sleep(.05)


# async def get_photo(message: Message, bot: Bot):
#     """Если получает фотку, то создает папку, если не создана с именем ID юзера, 
#     и закидывает фотку в эту папку, название фотки - дата и время отправки.
#     """
#     await message.answer(f'<em>Ты отправил картинку, я сохраню ее</em>')
#     file = await bot.get_file(message.photo[-1].file_id)
#     if not os.path.exists(f'users_photos/{message.from_user.id}'):
#         print('####')
#         os.chdir('users_photos')
#         os.mkdir(f'{message.from_user.id}')
#         os.chdir("/Users/Nikita/Desktop/New_profession/Боты")
#     await bot.download_file(file.file_path, f'users_photos/{message.from_user.id}/{datetime.now()}+.jpg')


# async def get_keyboard(message: Message, bot: Bot):
#     await message.answer('Вот интересная клава', reply_markup=loc_tel_q) 


# async def get_another_keyboard(message: Message, bot: Bot):
#     await message.answer('Вот другая интересная клава', reply_markup=get_reply_keyboard())


# async def get_location(message: Message, bot: Bot):
#     await message.answer(f'Ты отправил локацию\r\a'
#                          f'{message.location.latitude}\r\n{message.location.longitude}')

# async def get_hello(message: Message, bot: Bot):
#     await message.answer('И тебе привет человек!', reply_markup=reply_keyboard2)   


# async def get_contact(message: Message, bot: Bot):
#     if message.contact.user_id == message.from_user.id:
#         await message.answer(f'Ты отправил <b>свой</b> контакт{message.contact.phone_number}')     
#     else:
#         await message.answer(f'Ты отправил <b>не свой</b> контакт {message.contact.phone_number}')    

# async def get_inline(message: Message, bot: Bot):
#     await message.answer(f'Привет {message.from_user.first_name}, показываю inline клавиатуру',
#                           reply_markup=select_course) # reply_markup=select_course



# async def save_in_db(message: Message, bot: Bot, session: AsyncSession):
#     if not list(await session.execute(select(UserModel).filter_by(tg_id=message.from_user.id))):
#         await session.execute(
#             insert(UserModel).values(tg_id=message.from_user.id,
#                                      name=message.from_user.first_name)
#         )
#         await session.commit()
#         await message.answer('id занесен в базу')
#     else:
#         await message.answer('id уже был в базе')

        # async def save_in_db(message: Message, bot: Bot):
#     async with session() as session:
#         async with db_session.begin():
#             exists = await db_session.scalar(
#                 select(exists().where(UserModel.tg_id == message.from_user.id))
#             )
#             if not exists:
#                 await db_session.merge(
#                     UserModel(tg_id=message.from_user.id, name=message.from_user.first_name)
#                 )
#                 await message.answer('id занесен в базу')
#             else:
#                 await message.answer('id уже был в базе')
