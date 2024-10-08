import io
from typing import Optional, Union

import aiofiles
from aiogram import Bot, types
from aiogram.types import InputFile, BufferedInputFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.database import engine
from app.api.models import User, Application
from app.api.routers.user import router_user, update_user_balance
from app.api.routers.application import router_application
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView

from app.api.repositories.user import UserRepository

from app.config import TOKEN_BOT

class CallbackRequest(BaseModel):
    type: str
    invoiceId: str
    sessionId: str
    currency: str
    amount: str
    amountWithFee: str
    paymentId: Optional[str] = None
    amountUsdt: Optional[str] = None
    amountUsdtWithFee: Optional[str] = None
    externalText: Optional[str] = None
    status: Optional[str] = None
    timestampSeconds: str
    signature: str

user_repo = UserRepository()
app = FastAPI()
admin = Admin(app, engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.processing_balance, User.referal_balance, User.referer_id]

class ApplicationAdmin(ModelView, model=Application):
    column_list = [Application.id, Application.amount, Application.to_address]


admin.add_view(UserAdmin)
admin.add_view(ApplicationAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Список доменов, которым разрешен доступ. Можно использовать ["*"] для всех доменов.
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешенные заголовки
)

app.include_router(router_user)
app.include_router(router_application)

bot = Bot(token=TOKEN_BOT)



# Обработчик ошибок
def error_handler(error: str) -> None:
    print("errorHandler", error)

# Проверка метода POST
def is_post_method(req: Request) -> bool:
    return req.method == 'POST'

# Проверка наличия multipart/form-data
def is_multipart_form_data(req: Request) -> bool:
    return 'multipart/form-data' in req.headers.get('content-type', '')

# Обработка данных формы
async def process_form_data(status: str, id_gen: str, time_gen: str, res_image: UploadFile):
    try:
        if status != '200':
            raise HTTPException(status_code=400, detail="Invalid status")

        print(f"processFormData ID: {id_gen}, Time: {time_gen}")

        # Отправка изображения в Telegram
        await send_image_to_telegram(res_image, id_gen)
    except Exception as err:
        error_handler(str(err))

# Отправка изображения в Telegram
async def send_image_to_telegram(image: UploadFile, CHAT_ID):
    image_bytes = await image.read()

    # Create an InputFile object using BytesIO
    input_file = BufferedInputFile(image_bytes, filename=image.filename)

    # Send the photo to the Telegram chat
    await bot.send_photo(chat_id=CHAT_ID, photo=input_file)

@app.post("/webhook")
async def handle_webhook(
    request: Request,
    status: str = Form(...),
    id_gen: str = Form(...),
    time_gen: str = Form(...),
    res_image: UploadFile = File(...)
):
    if not is_post_method(request):
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    if not is_multipart_form_data(request):
        raise HTTPException(status_code=400, detail="Bad Request")
    print(type(res_image.file))
    await process_form_data(status, id_gen, time_gen, res_image)
    return JSONResponse(content={"message": "OK"}, status_code=200)

@app.get("/")
async def handle_webhook():
    return {"status": "kaif"}



@app.post("/merchant/callback")
async def handle_callback(callback: CallbackRequest):
    callback_body = callback.dict()
    id_chat = callback_body.get("externalText").split("_")[0]
    await user_repo.update_user_balance(id_chat, int(callback_body.get("externalText").split("_")[1]), 1)
    await bot.send_message(chat_id=id_chat, text=f"Баланс пополнен на {int(callback_body.get('externalText').split('_')[1])} обработок")
    usr = await user_repo.read_user(id_chat)
    if usr.referer_id != "0":
        await user_repo.update_user_balance(usr.referer_id, int(int(callback_body.get("amountUsdt"))*0.3), 0)
        await bot.send_message(usr.referer_id, f"Вам начислен бонус {int(int(callback_body.get('amountUsdt'))*0.3)} USDT за пополнение реферала")
