from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(
            'mysql+aiomysql://root:.Cosmos534534@localhost/TelegramBot',
            pool_pre_ping=True,)

session_maker = async_sessionmaker(
    bind=engine, autoflush=False, class_=AsyncSession,
    autocommit=False, expire_on_commit=False
)
