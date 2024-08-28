from ..schemas.user import UserIn
from app.api.repositories.user import UserRepository

class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo: UserRepository = user_repo

    async def create(self, schemas: UserIn):
        stmt = await self.user_repo.create_user(schemas)
        return stmt

    async def read(self, user_id: str):
        query = await self.user_repo.read_user(user_id)
        return query

    async def update(self, user_id: str, new_balance: int):
        stmt = await self.user_repo.update_user_balance(user_id, new_balance)
        return stmt