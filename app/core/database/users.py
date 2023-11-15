from sqlalchemy import VARCHAR, Integer, Text, Column, update, DateTime, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True)
    name = Column(Text(250), nullable=True)
    full_name = Column(Text(64), nullable=True)
    course = Column(Text(30), nullable=True)
    sp_club = Column(Text(30), nullable=True)
    arrears = Column(Integer, nullable=True)
    state = Column(VARCHAR(length=6), nullable=False, default='member')
    date = Column(DateTime, nullable=True)

    
    def __repr__(self):
        return "({}, {})".format(self.id, repr(self.name))

    @staticmethod
    async def update_state(session: AsyncSession, user_id: int, state: str) -> None:
        await session.execute(update(UserModel).where(UserModel.tg_id == user_id).values(state=state))
        await session.commit()

    @staticmethod
    async def update_arrears(session: AsyncSession, tg_id: int, arrears: int) -> None:
        await session.execute(update(UserModel).where(UserModel.tg_id == tg_id).values(arrears=arrears))
        await session.commit()


