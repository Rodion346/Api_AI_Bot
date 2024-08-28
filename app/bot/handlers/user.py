from operator import index

from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

bot = Bot(token='6830235739:AAG0Bo5lnabU4hDVWlhPQmLtiMVePI2xRGg')
router = Router()

button_options = {
    'age': ['Возраст - 18', 'Возраст - 20', 'Возраст - 30', 'Возраст - 40', 'Возраст - 50'],
    'breastSize': ['Размер груди - маленькая', 'Размер груди - Нормальня', 'Размер груди - Большая'],
    'bodyType': ['Телосложение - маленькое', 'Телосложение - нормальное', 'Телосложение - большое'],
    'buttSize': ['Размер попы - маленькая', 'Размер попы - Нормальня', 'Размер попы - Большая']
}


# Создаем инлайн клавиатуру
async def create_keyboard():
    markup = InlineKeyboardBuilder()
    for button_name, options in button_options.items():
        current_text = options[0]
        button = InlineKeyboardButton(text=current_text, callback_data=f'option_{button_name}')
        markup.row(button)
    markup.row(InlineKeyboardButton(text="Отправить", callback_data='send'))
    return markup


# Обработчик нажатия на кнопку
@router.callback_query(lambda c: 'option_' in c.data)
async def process_callback_button(call: CallbackQuery):
    button_name = call.data.split('_')[1]
    options = button_options[button_name]

    for row in call.message.reply_markup.inline_keyboard:
        for button in row:
            if button.text in options:
                current_index = options.index(button.text)
                new_index = (current_index + 1) % len(options)

                if options[new_index] != button.text:
                    button.text = options[new_index]
                    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
                    break

    await call.answer()


# Обработчик нажатия на кнопку "Отправить"
@router.callback_query(lambda c: c.data == 'send')
async def process_send(call: CallbackQuery):
    selected_options = {}
    for button_name, options in button_options.items():
        for row in call.message.reply_markup.inline_keyboard:
            for button in row:
                if button.text in options:
                    ind = button.text.index("-") + len("-")
                    selected_options[button_name] = button.text[ind:].replace(" ", "")

    await call.message.edit_reply_markup(reply_markup=None)  # Убираем кнопки
    await call.message.answer(f"Вы выбрали: {selected_options}")


# Обработчик команды /start
@router.message(Command('start'))
async def process_start_command(message: types.Message):
    kb = await create_keyboard()
    await message.answer('Привет! Выбери вариант:', reply_markup=kb.as_markup())


