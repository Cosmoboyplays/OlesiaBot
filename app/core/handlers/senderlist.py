import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from app.core.keyboards.reply import get_main_reply
from app.core.utils.google_api import service, spreadsheet_id
from app.core.utils.newletters import NewsletterManager
from aiogram.fsm.context import FSMContext

from app.core.database.users import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.config import load_config
from app.core.utils.reg_state import StepsForm
config = load_config()



class SenderList:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_message_inner(self, user_id, message_id, from_chat_id, name_camp, options: str, users_ids, text=None ):
        try:
            if options=='Разослать подтверждение курса/клуба':
                await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=get_main_reply())
            elif options=='Разослать стоимости':
                await self.bot.send_message(user_id, f'{text}\nК оплате: {users_ids[user_id]}р.')  
            else:    
                await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=None)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await self.send_message_inner(user_id, message_id, from_chat_id, name_camp, options)    
        

    async def broadcaster(self, message_id=None, from_chat_id=None, name_camp=None, options=None, users_ids=None, text=None):
        newsletter_manager = NewsletterManager()
        count = 0

        try:     
            newsletter_manager.start() # Запись ключа started на true
            old_users = newsletter_manager.get_users()  # Список пользователей которым уже было разослано сообщение

            for user_id in users_ids:
                if user_id in old_users:                 # Если пользователю уже было разослано сообщение, ничего не делать (continue)
                    continue
                await self.send_message_inner(user_id, message_id, from_chat_id, name_camp, options, users_ids, text=text)   # Если не было разослано сообщение, то добавить 
                newsletter_manager.add_user(user_id)  
                count += 1                                           # Добавить пользователя в список разосланных
                await asyncio.sleep(.05)

        except (Exception,):
            ...
        finally:
            # Запись ключа started на false
            newsletter_manager.stop()
            return count

           
    async def calculation(self, sheet_name, session: AsyncSession):
        try:
            users = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                range=f"'{sheet_name}'!A2:E300",         # формат "'Лист2'!A1:E10"
                                                majorDimension='ROWS'
                                                ).execute()
            
            values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                             range="'Стоимости'!A2:D18",         # формат "'Лист2'!A1:E10"
                                             majorDimension='ROWS'
                                             ).execute()
            
            course_data = dict([(i[0], i[1]) for i in values['values'] if len(i)>0]) # делаем словарь {'name':'цена'}
            new_sp = [i + [int(course_data.get(i[3], 0)) + int(course_data.get(i[4], 0))] for i in users['values'] if len(i) > 0]
            
            users = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                body = {"valueInputOption": "USER_ENTERED",
                                                        "data": [
                                                                {"range": f"'{sheet_name}'!A2:F300",
                                                                "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
                                                                "values": new_sp}
                                                                ]
                                                        }).execute()
            
            for i in new_sp:
                result = await session.execute(select(UserModel).filter_by(tg_id=i[0]))
                user = result.scalar_one_or_none()
                if user:
                    user.arrears = i[5]
                await session.commit()

            await  self.bot.send_message(config.bot.ADMIN_ID, text='Расчет окончен')
        except Exception:
            await  self.bot.send_message(config.bot.ADMIN_ID, text='Либо лист неправильно написан, либо все пропало')



    async def send_sum(self, sheet_name: str, text: str, options: str):
        users = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                range=f"'{sheet_name}'!A2:F300",         # формат "'Лист2'!A1:E10"
                                                majorDimension='ROWS'
                                                ).execute()
        
        values = dict([(i[0], i[5]) for i in users['values']])
        count = await self.broadcaster(options=options, users_ids=values, text=text)
        return count
            
        # newsletter_manager = NewsletterManager()
        # count = 0

        # try:     
        #     newsletter_manager.start() # Запись ключа started на true
        #     old_users = newsletter_manager.get_users()  # Список пользователей которым уже было разослано сообщение

        #     for user_id in users_ids:
        #         if user_id[0] in old_users:                 # Если пользователю уже было разослано сообщение, ничего не делать (continue)
        #             continue
        #         await self.send_message(user_id[0], message_id, from_chat_id, name_camp, options)   # Если не было разослано сообщение, то добавить 
        #         newsletter_manager.add_user(user_id[0])  
        #         count += 1                                           # Добавить пользователя в список разосланных
        #         await asyncio.sleep(.05)

        # except (Exception,):
        #     ...
        # finally:
        #     # Запись ключа started на false
        #     newsletter_manager.stop()
        #     return count

        
        

        
    # async def send_calc(self):
    #     users = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
    #                                          range="'Лист1'!A2:F300",         # формат "'Лист2'!A1:E10"
    #                                          majorDimension='ROWS'
    #                                          ).execute()
        