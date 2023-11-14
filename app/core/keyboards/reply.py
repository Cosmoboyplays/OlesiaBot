from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.core.utils.text import TextButton


def get_main_reply():
    k_b = ReplyKeyboardBuilder()
    k_b.button(text='Подтвердить выбор курса :)|')
    k_b.button(text='Отправь кота')

    k_b.adjust(1)
    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_cat_reply():
    k_b = ReplyKeyboardBuilder()
    k_b.button(text='Отправь кота')

    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=False)


def get_reply_courses():
    k_b = ReplyKeyboardBuilder()
    k_b.button(text='"C нуля" ENG - пятница 18:00')
    k_b.button(text='"А1" ENG воскресенье 13:00')
    k_b.button(text='"А1-А2" ENG вторник 18:00')
    k_b.button(text='"А2" ENG среда 18:30')
    k_b.button(text='"В1+" ENG вторник 18:00')
    k_b.button(text='"В2" ENG четверг 18:30')
    k_b.button(text='Я только в разговорный клуб')
    k_b.button(text='Я не знаю')

    k_b.adjust(1)
    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Какой курс?')


def get_reply_spclub():
    k_b = ReplyKeyboardBuilder()
    k_b.button(text='SC 1 "А1-А2" ENG пятница 18:30')
    k_b.button(text='SC 2 "В1-В2" ENG пятница 18:30')
    k_b.button(text='SC 3 "С1" ENG понедельник 18:00')
    k_b.button(text='Мне не нужен разговорный клуб')
    k_b.button(text='Я не знаю')

    k_b.adjust(1)
    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Какой клуб?')


def get_reply_confirm():
    k_b = ReplyKeyboardBuilder()
    k_b.button(text='Да')
    k_b.button(text='Нет')

    k_b.adjust(2)
    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Да/Нет')


def get_admin_reply():
    k_b = ReplyKeyboardBuilder()
    k_b.button(text=TextButton.send_simple_message)
    k_b.button(text='Разослать подтверждение курса/клуба')
    k_b.button(text='Рассчитать стоимости')
    k_b.button(text='Разослать стоимости')
    k_b.button(text='Рассылка по листу')

    k_b.adjust(1)
    return k_b.as_markup(resize_keyboard=True, one_time_keyboard=True,
                         input_field_placeholder='Да/Нет')

# reply_keyboard = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(
#             text='Покажи интересную клавиатуру'
#         ),
#         KeyboardButton(
#             text='Ряд 1, кнопка 2'
#         ),
#         KeyboardButton(
#             text='Ряд 1, кнопка 3'
#         )
#     ],
#     [
#         KeyboardButton(
#             text='Покажи другую интересную клавиатуру'
#         ),
#         KeyboardButton(
#             text='Ряд 2, кнопка 2'
#         )
#     ],
#         [
#         KeyboardButton(
#             text='Ряд 3, кнопка 1'
#         )
#     ]
# ])

# reply_keyboard2 = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(
#             text='Ряд 100, кнопка 1'
#         ),
#         KeyboardButton(
#             text='Ряд 100, кнопка 2'
#         ),
#         KeyboardButton(
#             text='Ряд 100, кнопка 3'
#         )
#     ]
# ], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите кнопку ↓', selective=True)

# loc_tel_q = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(
#             text='Отправить геолокацию',
#             request_location=True
#         )
#     ],
#     [
#         KeyboardButton(
#             text='Отправить свой контакт',
#             request_contact=True
#         )
#     ],
#     [
#         KeyboardButton(
#             text='Создать викторину',
#             request_poll=KeyboardButtonPollType()
#         )
#     ]
# ], resize_keyboard=True, one_time_keyboard=False, 
# input_field_placeholder='Отправьте локацию или номер телефона или создайте викторину/опрос')


# Другой способ создания клавы

# def get_reply_keyboard():
#     k_b = ReplyKeyboardBuilder()
#     k_b.button(text='Отправь кота')
#     # k_b.button(text='Рассылка')
#     # k_b.button(text='Сохрани контакт')
#     # k_b.button(text='Локация', request_location=True)
#     # k_b.button(text='Мой контакт', request_contact=True)
#     k_b.adjust(1)
#     return k_b.as_markup(resize_keyboard=True, one_time_keyboard=False, 
#                  input_field_placeholder='Отправьте локацию или номер телефона или создайте викторину/опрос')
