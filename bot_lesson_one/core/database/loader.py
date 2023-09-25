from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+pymysql://root:.Cosmos534534@localhost/TelegramBot'
)

session_maker = sessionmaker(
    bind=engine, autoflush=False,
    autocommit=False, expire_on_commit=False
)
