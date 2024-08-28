import aiofiles
from aiogram import Bot, types
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.user import router_user
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Список доменов, которым разрешен доступ. Можно использовать ["*"] для всех доменов.
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешенные заголовки
)

app.include_router(router_user)

BOT_TOKEN = '6830235739:AAG0Bo5lnabU4hDVWlhPQmLtiMVePI2xRGg'
CHAT_ID = '6640814090'
bot = Bot(token=BOT_TOKEN)

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
        await send_image_to_telegram(res_image)
    except Exception as err:
        error_handler(str(err))

# Отправка изображения в Telegram
async def send_image_to_telegram(image: UploadFile):
    file_bytes = await image.read()
    await bot.send_photo(CHAT_ID, types.InputFile(image.filename, file_bytes))

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

    await process_form_data(status, id_gen, time_gen, res_image)
    return JSONResponse(content={"message": "OK"}, status_code=200)
