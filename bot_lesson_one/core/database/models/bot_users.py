from database.models import Base
from sqlalchemy import Integer, Text, Column


class Bot_users(Base):
    __tablename__ = "bot_users"

    id_user = Column(Integer, primary_key=True)
    name = Column(Text(250), nullable=False)
    
    def __repr__(self):
        return "<{}:{}>".format(id, self.name)
