from app.api.repositories.user import UserRepository
from app.api.services.user import UserService


async def get_user_service() -> UserService:
    return UserService(UserRepository())