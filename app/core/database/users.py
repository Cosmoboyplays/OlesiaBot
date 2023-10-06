from sqlalchemy import Integer, Text, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    name = Column(Text(250), nullable=False)
    
    def __repr__(self):
        return "({}, {})".format(self.id, repr(self.name))
