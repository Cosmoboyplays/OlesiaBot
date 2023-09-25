from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Покажи интересную клавиатуру'
        ),
        KeyboardButton(
            text='Ряд 1, кнопка 2'
        ),
        KeyboardButton(
            text='Ряд 1, кнопка 3'
        )
    ],
    [
        KeyboardButton(
            text='Покажи другую интересную клавиатуру'
        ),
        KeyboardButton(
            text='Ряд 2, кнопка 2'
        )
    ],
        [
        KeyboardButton(
            text='Ряд 3, кнопка 1'
        )
    ]
])

reply_keyboard2 = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Ряд 100, кнопка 1'
        ),
        KeyboardButton(
            text='Ряд 100, кнопка 2'
        ),
        KeyboardButton(
            text='Ряд 100, кнопка 3'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите кнопку ↓', selective=True)

loc_tel_q = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить геолокацию',
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text='Отправить свой контакт',
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text='Создать викторину',
            request_poll=KeyboardButtonPollType()
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, 
input_field_placeholder='Отправьте локацию или номер телефона или создайте викторину/опрос')


# Другой способ создания клавы

def get_reply_keyboard():
    k_b = ReplyKeyboardBuilder()

    k_b.button(text='Кнопка 1')
    k_b.button(text='Кнопка 2')
    k_b.button(text='Кнопка 3')
    k_b.button(text='Локация', request_location=True)
    k_b.button(text='Мой контакт', request_contact=True)

    k_b.adjust(3, 1, 1)
    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=False, 
                 input_field_placeholder='Отправьте локацию или номер телефона или создайте викторину/опрос')
