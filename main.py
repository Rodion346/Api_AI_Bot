import aiofiles
from aiogram import Bot, Dispatcher
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.user import router_user
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()

bot = Bot(token='6830235739:AAG0Bo5lnabU4hDVWlhPQmLtiMVePI2xRGg')
dp = Dispatcher(bot)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Список доменов, которым разрешен доступ. Можно использовать ["*"] для всех доменов.
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешенные заголовки
)

app.include_router(router_user)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def error_handler(error: str) -> None:
    """
    Handles errors by logging the error message.
    @param error: The error message to log.
    """
    print("errorHandler", error)

async def send_image_to_telegram(file_path: str) -> None:
    """
    Sends an image to a specified Telegram chat.
    @param file_path: The path to the image file to send.
    """
    try:
        async with aiofiles.open(file_path, 'rb') as image_file:
            await bot.send_photo(chat_id=6640814090, photo=image_file)
        print(f"Image sent to Telegram chat ID: {6640814090}")
    except Exception as err:
        error_handler(f"Failed to send image to Telegram: {err}")

def process_form_data(status: str, id_gen: str, time_gen: str, res_image: UploadFile) -> str:
    """
    Processes the form data from the request.
    @param status: The status from the form data.
    @param id_gen: The ID from the form data.
    @param time_gen: The generation time from the form data.
    @param res_image: The uploaded file from the form data.
    @returns: The file path where the image is saved.
    """
    try:
        if status != '200':
            raise Exception("Image generation failed")
        elif res_image.filename == '':
            raise Exception("resImage is not a file")

        file_path = os.path.join(UPLOAD_FOLDER, 'resImage.png')
        with open(file_path, "wb") as buffer:
            buffer.write(res_image.file.read())

        print("processFormData", f"ID: {id_gen}, Time: {time_gen}")
        return file_path
    except Exception as err:
        error_handler(str(err))
        raise HTTPException(status_code=400, detail=str(err))


@app.post('/webhook')
async def handle_webhook(
    status: str = Form(...),
    id_gen: str = Form(...),
    time_gen: str = Form(...),
    res_image: UploadFile = File(...)
):
    """
    Main handler function for the webhook endpoint.
    @param status: The status from the form data.
    @param id_gen: The ID from the form data.
    @param time_gen: The generation time from the form data.
    @param res_image: The uploaded file from the form data.
    @returns: A JSON response indicating the result of the request handling.
    """
    file_path = process_form_data(status, id_gen, time_gen, res_image)
    await send_image_to_telegram(file_path)
    return JSONResponse(content={"message": "OK"}, status_code=200)