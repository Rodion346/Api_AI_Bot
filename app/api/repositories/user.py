from sqlalchemy import select, update

from app.api.schemas.user import UserIn
from app.api.database import async_session_maker
from app.api.models import User


class UserRepository:
    model = User

    async def create_user(self, schemas: UserIn):
        async with async_session_maker() as session:
            stmt = self.model(**schemas.dict())
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt


    async def read_user(self, user_id: str):
        async with async_session_maker() as session:
            query = select(self.model)
            user = await session.execute(query.filter(self.model.id == user_id))
            user = user.scalars().first()
            return user


    async def update_user_balance(self, user_id: str, new_balance: int):
        async with async_session_maker() as session:
            await session.execute(update(self.model).where(self.model.id == user_id).values(balance=new_balance))
            query = select(self.model)
            user = await session.execute(query.filter(self.model.id == user_id))
            stmt = user.scalars().first()
            await session.commit()
            return stmt
