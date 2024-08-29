import subprocess

from fastapi import APIRouter, Depends

from .depence import get_user_service
from app.api.schemas.user import UserIn, UserOut
from app.api.services.user import UserService


router_user = APIRouter(tags=["User"], prefix="/api/v1")



@router_user.get("/db")
async def create_user():
    result = subprocess.run(['alembic', 'upgrade', 'head'], check=True, capture_output=True, text=True)
    return result

@router_user.post("/user", response_model=UserOut)
async def create_user(user: UserIn, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create(user)
    return user

@router_user.post("/user/{user_id}", response_model=UserOut)
async def update_user_balance(user_id: str, new_balance: int, user_service: UserService = Depends(get_user_service)):
    user_info = await user_service.update(user_id, new_balance)
    return user_info

@router_user.get("/user/{user_id}", response_model=UserOut)
async def get_user_info(user_id: str, user_service: UserService = Depends(get_user_service)):
    user_info = await user_service.read(user_id)
    return user_info

