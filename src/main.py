import asyncio

from domain.entities import User
from infrastructure.configs import settings
from infrastructure.database.repositories import SQLAchemyUserRepository
from infrastructure.database import sessionmanager


async def async_main() -> None:
    async with sessionmanager.session() as session:
        print(settings)
        repo = SQLAchemyUserRepository(session)
        user = await repo.save(User(user_id=1,name="test"))

        print(user)


if __name__ == "__main__":
    asyncio.run(async_main())
