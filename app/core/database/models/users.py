from app.core.database.models import Base
from sqlalchemy import Integer, Text, Column


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    name = Column(Text(250), nullable=False)
    
    def __repr__(self):
        return "<{}:{}>".format(id, self.name)
