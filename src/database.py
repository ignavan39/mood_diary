from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from configs.config import settings

database_url = settings.get_db_config().get_url()

engine = create_async_engine(url=database_url,echo=True)
async_session = async_sessionmaker(engine,class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
