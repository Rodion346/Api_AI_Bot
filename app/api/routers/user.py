import asyncio
import subprocess

import requests
from aiogram import Bot
from aiogram.types import BufferedInputFile
from fastapi import APIRouter, Depends
from flask import request
from sqlalchemy.testing.suite.test_reflection import users
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


from .depence import get_user_service
from app.api.schemas.user import UserIn, UserOut
from app.api.services.user import UserService


router_user = APIRouter(tags=["User"], prefix="/api/v1")

BOT_TOKEN = '6830235739:AAG0Bo5lnabU4hDVWlhPQmLtiMVePI2xRGg'
bot = Bot(token=BOT_TOKEN)


async def niked(img_id: str, user_id: str):
    while True:
        resp = requests.get(f"https://use.n8ked.app/api/deepnude/{img_id}")
        resp = resp.json()
        stat = resp.get("status")
        if stat == "completed":
            bas64: str = resp.get("output")
            img64 = bas64.split(",")
            img6 = img64[1].strip()
            await bot.send_photo(chat_id=user_id, photo=img6)
        else: await asyncio.sleep(5)


@router_user.post("/niked/{img_id}")
async def get_niked_img(img_id: str, user_id: str):
    task = BackgroundTask(niked, img_id, user_id)
    return JSONResponse({"status": "ok"}, background=task)

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

