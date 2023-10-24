from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.users import UserModel


async def my_chat_member(update: ChatMemberUpdated,
                         session: AsyncSession) -> None:
    await UserModel.update_state(session, user_id=update.from_user.id, state=update.new_chat_member.status)
