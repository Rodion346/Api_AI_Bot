from ..schemas.application import ApplicationIn
from app.api.repositories.application import ApplicationRepository

class ApplicationService:

    def __init__(self, applic_repo: ApplicationRepository):
        self.applic_repo: ApplicationRepository = applic_repo

    async def create(self, schemas: ApplicationIn):
        stmt = await self.applic_repo.create_application(schemas)
        return stmt

    async def read(self, user_id: str):
        query = await self.applic_repo.read_application(user_id)
        return query
