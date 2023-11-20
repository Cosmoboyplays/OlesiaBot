import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from app.core.keyboards.reply import get_main_reply
from app.core.utils.google_api import service, spreadsheet_id, GoogleTable
from app.core.utils.newletters import NewsletterManager
from aiogram.fsm.context import FSMContext

from app.core.database.users import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.config import load_config
from app.core.utils.reg_state import StepsForm
from app.core.utils.text import TextButton

config = load_config()

from aiogram.fsm.storage.base import StorageKey


##

class SenderList:
    def __init__(self, bot: Bot, dp) -> None:
        self.bot = bot
        self.dp = dp

    async def send_message_inner(self, data, user_id, users_ids):
        print('111')
        message_id = data.get('message_id', None)
        from_chat_id = data.get('chat_id', None)
        options = data.get('options', None)
        key_confirm = data.get('key_confirm', None)
        text = data.get('text', None)
        print('222')

        try:
            if options == TextButton.send_confirm:
                await self.bot.copy_message(user_id, int(from_chat_id), int(message_id), reply_markup=get_main_reply())

            elif options == TextButton.send_by_sheet:
                if key_confirm == 1:
                    await self.bot.copy_message(user_id, int(from_chat_id), int(message_id),
                                                reply_markup=get_main_reply())
                elif key_confirm is None:
                    await self.bot.copy_message(user_id, int(from_chat_id), int(message_id), reply_markup=None)

            elif options == TextButton.send_price:
                state = FSMContext(self.dp.storage,
                                   key=StorageKey(bot_id=self.bot.id, chat_id=int(user_id), user_id=int(user_id)))
                await self.bot.send_message(user_id, f'{text}\nК оплате: {users_ids[user_id][-1]}р.', reply_markup=None)
                await state.set_state(StepsForm.GET_PAY)
                await state.update_data(full_name=users_ids[user_id][0])
            else:
                await self.bot.copy_message(user_id, int(from_chat_id), int(message_id), reply_markup=None)

        except TelegramBadRequest as e:
            print(e)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await self.send_message_inner(data, user_id, users_ids)

    async def broadcaster(self, data: dict, users_ids):
        newsletter_manager = NewsletterManager()
        newsletter_manager.start()  # Запись ключа started на true
        old_users = newsletter_manager.get_users()  # Список пользователей которым уже было разослано сообщение
        count = 0

        for user_id in users_ids:
            if user_id in old_users:  # Если пользователю уже было разослано сообщение, ничего не делать (continue)
                continue

            try:
                await self.send_message_inner(data, user_id, users_ids)  # Если не было разослано сообщение, то добавить
                newsletter_manager.add_user(user_id)
                count += 1  # Добавить пользователя в список разосланных
                await asyncio.sleep(.05)
            except Exception as e:
                print("При блокировке:", e)

        newsletter_manager.stop()
        return count

    async def calculation(self, sheet_name, session: AsyncSession):
        """Считаем сколько должен человек.

        пишем в базу и в google sheets"""
        gt = GoogleTable()
        try:
            users = gt.get_data(f"'{sheet_name}'!A2:F300")
            values = gt.get_data("'Стоимости'!A2:D18")
            course_data = dict([(i[0], i[1]) for i in values['values'] if len(i) > 0])  # {'name_club':'цена'}
            new_sp = [i + [int(course_data.get(i[3], 0)) + int(course_data.get(i[4], 0)) + int(course_data.get(i[5], 0))]
                      for i in users['values'] if len(i) > 0]  # анг + sc + spain
            users = gt.batchUpdate(f"'{sheet_name}'!A2:G300", new_sp)

            try:
                for i in new_sp:
                    result = await session.execute(select(UserModel).filter_by(tg_id=i[0]))
                    user = result.scalar_one_or_none()
                    if user:
                        user.arrears = i[6]
                    await session.commit()
            except Exception:
                await  self.bot.send_message(config.bot.ADMIN_ID, text='Не могу писать в базу, зови разраба.')

            await  self.bot.send_message(config.bot.ADMIN_ID, text='Расчет окончен')

        except Exception as e:
            await  self.bot.send_message(config.bot.ADMIN_ID, text='Либо лист неправильно написан, либо все пропало')

    async def send_by_sheet(self, data: dict):
        sheet_name = str(data.get('sheet_name'))
        users = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                    range=f"'{sheet_name}'!A2:G300",  # формат "'Лист2'!A1:E10"
                                                    majorDimension='ROWS'
                                                    ).execute()
        if data.get('options', None) == TextButton.send_price:
            values = dict([(i[0], (i[2], i[6])) for i in users['values']])
            values = {key: value for key, value in values.items() if value[-1] != '0'}
        else:
            values = [i[0] for i in users['values']]
        count = await self.broadcaster(data, users_ids=values)
        return count
