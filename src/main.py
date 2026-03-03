import asyncio
import datetime

from configs.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.entities.diary import Diary
from infrastructure.database.data_mappers.diary import diary_entity_to_model


async def async_main():
    database_url = settings.get_db_config().get_url()
    engine = create_async_engine(url=database_url, echo=True)
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    print(settings)
    print(diary_entity_to_model(Diary(date = datetime.datetime.now().date, rating=2, user_id=2)))

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
