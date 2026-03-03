import asyncio

from configs.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from configs.config import settings

async def async_main():
    database_url = settings.get_db_config().get_url()
    engine = create_async_engine(url=database_url,echo=True)
    async_session = async_sessionmaker(engine,class_=AsyncSession, expire_on_commit=False)
    print(settings)

    await engine.dispose()


if __name__ == "__main__":
     asyncio.run(async_main())
