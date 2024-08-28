from aiogram import types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Нейронка 1", callback_data="AI1"))
    builder.add(types.InlineKeyboardButton(text="Нейронка 2", callback_data="AI2"))
    await message.answer("start_txt", reply_markup=builder.as_markup())