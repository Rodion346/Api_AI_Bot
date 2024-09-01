import asyncio
import base64

import requests
from aiogram import Bot
from aiogram.types import BufferedInputFile
from fastapi import APIRouter, Depends

from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


from .depence import get_user_service
from app.api.schemas.user import UserIn, UserOut
from app.api.services.user import UserService
from app.config import TOKEN_BOT

router_user = APIRouter(tags=["User"], prefix="/api/v1")


bot = Bot(token=TOKEN_BOT)
header = {'Authorization': 'Bearer zsWQ5mwIh7BvrcoNDbrjU6eU2EvqicvDJdIz8LmZ88225bcf'}


async def niked(img_id: str, user_id: str):
    a = 0
    while a == 0:
        resp = requests.get(f"https://use.n8ked.app/api/deepnude/{img_id}", headers=header)
        resp = resp.json()
        stat = resp.get("status")
        if stat == "completed":
            bas64: str = resp.get("output")
            img64 = bas64.split(",")
            img6 = img64[1].strip()
            img6_1 = img6.encode()
            last = base64.b64decode(img6_1)
            input_file = BufferedInputFile(last, filename=f"{user_id}")
            await bot.send_photo(chat_id=user_id, photo=input_file)
            a = 1
        else: await asyncio.sleep(5)


@router_user.post("/niked")
async def get_niked_img(img_id: str, user_id: str):
    task = BackgroundTask(niked, img_id, user_id)
    return JSONResponse({"status": "ok"}, background=task)

@router_user.post("/user", response_model=UserOut)
async def create_user(user: UserIn, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create(user)
    return user

@router_user.post("/user/{user_id}", response_model=UserOut)
async def update_user_balance(user_id: str, new_balance: int, type_balance: int, user_service: UserService = Depends(get_user_service)):
    user_info = await user_service.update(user_id, new_balance, type_balance)
    return user_info

@router_user.get("/user/{user_id}", response_model=UserOut)
async def get_user_info(user_id: str, user_service: UserService = Depends(get_user_service)):
    user_info = await user_service.read(user_id)
    return user_info

