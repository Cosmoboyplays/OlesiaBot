from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  
from aiogram.utils.keyboard import InlineKeyboardBuilder


select_course = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Обучение шейкер',
            callback_data='Информация о курсе'
        )
    ],
    [
        InlineKeyboardButton(
            text='Обучение джембе',
            callback_data='Информация о курсе'
        )
    ],
    [
        InlineKeyboardButton(
            text='Обучение ханг',
            callback_data='Информация о курсе'
        )
    ],
    [
        InlineKeyboardButton( 
            text='Вконтакте Cosmoboy',
            url='https://vk.com/im'
        )
    ],
    [
        InlineKeyboardButton( 
            text='Телега Cosmoboy',
            url='t.me/cosmoboyplays'
        )
    ]
])

def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    
    keyboard_builder.button(text='Обучение джембе', callback_data='Информация о курсе')
    keyboard_builder.button(text='Вконтакте Cosmoboy', url='https://vk.com/im')

    return keyboard_builder.as_markup()