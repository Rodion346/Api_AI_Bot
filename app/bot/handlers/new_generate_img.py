from aiogram import types, Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State



router = Router()

user_data = {}

class OrderTask(StatesGroup):
    age = State()
    breast_size = State()
    body_type = State()
    butt_size = State()
    pose = State()
    cloth = State()




@router.callback_query(F.data == "AI1")
async def generate_base(callback: types.CallbackQuery):
    await callback.answer("Пришлите фото для обработки")
    user_data[callback.from_user.id] = {}


@router.message(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, ждет ли пользователь отправки фото
    if user_id in user_data:
        # Получаем файл и его ID
        photo = message.photo[-1]  # Берем последнее фото (наибольшего разрешения)
        file_id = photo.file_id

        # Скачиваем файл на сервер
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        await message.bot.download_file(file_path, f"photos/{user_id}.jpg")

        await message.answer("Фото получено и сохранено.")

        # Здесь можно добавить логику для отправки фото в нейронную сеть
        # например, вызвать функцию из services/neural_networks/api1.py

        # Удаляем данные о пользователе, т.к. фото уже получено
        del user_data[user_id]
    else:
        await message.answer("Пожалуйста, используйте команду, чтобы начать процесс.")
