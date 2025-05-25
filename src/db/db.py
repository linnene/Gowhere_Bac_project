from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine, AsyncSession


# 数据库连接字符串
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 创建异步 Session 类
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

#获取数据库Session
async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

