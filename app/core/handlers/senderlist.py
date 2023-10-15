import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from app.core.keyboards.reply import get_main_reply
from app.core.utils.google_api import service, spreadsheet_id
from app.core.utils.newletters import NewsletterManager


class SenderList:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        print('Создал')

    async def send_message(self, user_id: int, message_id: int, from_chat_id: int, name_camp: str, options: str):
        try:
            if options=='Разослать подтверждение курса/клуба':
                await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=get_main_reply())
            else:    
                await self.bot.copy_message(user_id, from_chat_id, message_id)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await self.send_message(user_id, message_id, from_chat_id, name_camp, options)    
        

    async def broadcaster(self, message_id: int, from_chat_id: int, name_camp: str, options: str):
        newsletter_manager = NewsletterManager()

        values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                             range="'Лист1'!A2:E300",         # формат "'Лист2'!A1:E10"
                                             majorDimension='ROWS'
                                             ).execute()
        users_ids = [i[0] for i in values['values']]

        try:     
            newsletter_manager.start() # Запись ключа started на true
            old_users = newsletter_manager.get_users()  # Список пользователей которым уже было разослано сообщение

            for user_id in users_ids:
                if user_id in old_users:                 # Если пользователю уже было разослано сообщение, ничего не делать (continue)
                    continue
                await self.send_message(user_id, message_id, from_chat_id, name_camp, options)   # Если не было разослано сообщение, то добавить 
                newsletter_manager.add_user(user_id)                                     # Добавить пользователя в список разосланных
                await asyncio.sleep(.05)

        except (Exception,):
            ...
        finally:
            # Запись ключа started на false
            newsletter_manager.stop()
            print('Рассылка закончена')
