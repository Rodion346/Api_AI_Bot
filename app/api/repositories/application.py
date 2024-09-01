from sqlalchemy import select, update

from app.api.schemas.application import ApplicationIn
from app.api.database import async_session_maker
from app.api.models import Application


class ApplicationRepository:
    model = Application

    async def create_application(self, schemas: ApplicationIn):
        async with async_session_maker() as session:
            stmt = self.model(**schemas.dict())
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt


    async def read_application(self, user_id: str):
        async with async_session_maker() as session:
            query = select(self.model)
            user = await session.execute(query.filter(self.model.id == user_id))
            user = user.scalars().first()
            return user
