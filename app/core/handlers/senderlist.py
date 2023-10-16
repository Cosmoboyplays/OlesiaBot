import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from app.core.keyboards.reply import get_main_reply
from app.core.utils.google_api import service, spreadsheet_id
from app.core.utils.newletters import NewsletterManager
from sqlalchemy import select, insert
from app.core.database.users import UserModel
from sqlalchemy.ext.asyncio import AsyncSession

from pprint import pprint

class SenderList:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_message(self, user_id: int, message_id: int, from_chat_id: int, name_camp: str, options: str):
        try:
            if options=='Разослать подтверждение курса/клуба':
                await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=get_main_reply())
            else:    
                await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=None)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await self.send_message(user_id, message_id, from_chat_id, name_camp, options)    
        

    async def broadcaster(self, message_id: int, from_chat_id: int, name_camp: str, options: str, session: AsyncSession):
        newsletter_manager = NewsletterManager()

        # values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
        #                                      range="'Лист1'!A2:F300",         # формат "'Лист2'!A1:E10"
        #                                      majorDimension='ROWS'
        #                                      ).execute()
        query = select(UserModel.tg_id) # [i[0] for i in values['values'] if len(i)>0]
        users_ids = await session.execute(query)

        try:     
            newsletter_manager.start() # Запись ключа started на true
            old_users = newsletter_manager.get_users()  # Список пользователей которым уже было разослано сообщение

            for user_id in users_ids:
                if user_id[0] in old_users:                 # Если пользователю уже было разослано сообщение, ничего не делать (continue)
                    continue
                await self.send_message(user_id[0], message_id, from_chat_id, name_camp, options)   # Если не было разослано сообщение, то добавить 
                newsletter_manager.add_user(user_id[0])                                     # Добавить пользователя в список разосланных
                await asyncio.sleep(.05)

        except (Exception,):
            ...
        finally:
            # Запись ключа started на false
            newsletter_manager.stop()
            print('Рассылка закончена')

           
    async def calculation(self):
        values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                             range="'Лист1'!H2:J18",         # формат "'Лист2'!A1:E10"
                                             majorDimension='ROWS'
                                             ).execute()
        course_data = dict([(i[0], i[1]) for i in values['values'] if len(i)>0])

        users = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                             range="'Лист1'!A2:E300",         # формат "'Лист2'!A1:E10"
                                             majorDimension='ROWS'
                                             ).execute()
        
        new_sp = [i + [int(course_data.get(i[3], 0)) + int(course_data.get(i[4], 0))] for i in users['values'] if len(i) > 0]
        
        users = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                             body = {"valueInputOption": "USER_ENTERED",
                                                    "data": [
                                                            {"range": "A2:F300",
                                                            "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
                                                            "values": new_sp}
                                                            ]
                                                    }).execute()
        
    # async def send_calc(self):
    #     users = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
    #                                          range="'Лист1'!A2:F300",         # формат "'Лист2'!A1:E10"
    #                                          majorDimension='ROWS'
    #                                          ).execute()
        