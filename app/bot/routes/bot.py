from aiogram import Router, F, Bot, types

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
start_router = Router()


def create_keyboard(buttons, columns=2):
    keyboard_buttons = []
    for i in range(0, len(buttons), columns):
        row = [types.KeyboardButton(text=button) for button in buttons[i:i + columns]]
        keyboard_buttons.append(row)
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)

@start_router.message(Command('start'))
async def process_start_command(message: types.Message):
    payload = {"id": f"{message.from_user.id}", "referer_id": 0}
    requests.post("http://127.0.0.1:8000/api/v1/user", json=payload)
    buttons = ["Обработка фото", "Пополнить баланс", "Реферальная программа", "Профиль"]
    keyboard = create_keyboard(buttons, columns=1)
    await message.answer('Привет!', reply_markup=keyboard)


@start_router.message(F.text == "Обработка фото")
async def processing_image(message: types.Message):
    kb = InlineKeyboardBuilder()
    Button = InlineKeyboardButton(text='Умная', callback_data="smart")
    Button2 = InlineKeyboardButton(text='Простая', callback_data="simple")
    kb.row(Button)
    kb.row(Button2)
    await message.answer('Выберите режим:', reply_markup=kb.as_markup())

@start_router.message(F.text == "Профиль")
async def processing_image(message: types.Message):
    r = requests.get(f"http://127.0.0.1:8000/api/v1/user/{message.from_user.id}")
    re = r.json()
    id_user = re.get("id")
    balance = re.get("balance")
    await message.answer(f"ID: {id_user}\nБаланс: {balance}")