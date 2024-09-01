from app.api.repositories.user import UserRepository
from app.api.services.user import UserService
from app.api.services.application import ApplicationService
from app.api.repositories.application import ApplicationRepository


async def get_user_service() -> UserService:
    return UserService(UserRepository())

async def get_applicaton_service() -> ApplicationService:
    return ApplicationService(ApplicationRepository())