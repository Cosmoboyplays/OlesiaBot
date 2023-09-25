from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import reply_keyboard, reply_keyboard2, loc_tel_q, get_reply_keyboard
from core.keyboards.inline import select_course, get_inline_keyboard
from datetime import datetime
import os 



async def get_start(message: Message, bot: Bot, counter: str):
    await message.answer(f'Сообщение #{counter}')
    await message.answer(f'Привет <b>{message.from_user.first_name}. </b>', reply_markup=reply_keyboard) # просто ответ | второй аргумент это клава
    # await message.reply(f'Привет <b>{message.from_user.first_name}. </b>') # ответ с пересланным 


async def get_photo(message: Message, bot: Bot):
    """Если получает фотку, то создает папку, если не создана с именем ID юзера, 
    и закидывает фотку в эту папку, название фотки - дата и время отправки.
    """
    await message.answer(f'<em>Ты отправил картинку, я сохраню ее</em>')
    file = await bot.get_file(message.photo[-1].file_id)
    if not os.path.exists(f'users_photos/{message.from_user.id}'):
        print('####')
        os.chdir('users_photos')
        os.mkdir(f'{message.from_user.id}')
        os.chdir("/Users/Nikita/Desktop/New_profession/Боты")
    await bot.download_file(file.file_path, f'users_photos/{message.from_user.id}/{datetime.now()}+.jpg')


async def get_keyboard(message: Message, bot: Bot):
    await message.answer('Вот интересная клава', reply_markup=loc_tel_q) 


async def get_another_keyboard(message: Message, bot: Bot):
    await message.answer('Вот другая интересная клава', reply_markup=get_reply_keyboard()) 


async def get_location(message: Message, bot: Bot):
    await message.answer(f'Ты отправил локацию\r\a'
                         f'{message.location.latitude}\r\n{message.location.longitude}')
                         
async def get_hello(message: Message, bot: Bot):
    await message.answer('И тебе привет человек!', reply_markup=reply_keyboard2)   


async def get_contact(message: Message, bot: Bot):
    if message.contact.user_id == message.from_user.id:
        await message.answer(f'Ты отправил <b>свой</b> контакт{message.contact.phone_number}')     
    else:
        await message.answer(f'Ты отправил <b>не свой</b> контакт {message.contact.phone_number}')    

async def get_inline(message: Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name}, показываю inline клавиатуру',
                          reply_markup=select_course) # reply_markup=select_course
    
async def get_free_text(message: Message, bot: Bot):
    await message.answer('Ты отправил свободный текст')      