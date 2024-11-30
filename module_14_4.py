# ДЗ "Доработка бота"
# Цель: Подготовить Телеграм-бота для взаимодействия с базой данных
# Задача "Витамины для всех"


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import initiate_db, get_all_products
import os

api = '7896102855:AAHI1_Ozmi5PdqWVy9arpb1jibnmxwbFK9g'  # Ваш токен бота
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация базы данных при запуске бота
initiate_db()

# Основная клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_catalog = KeyboardButton(text='Перейти в каталог продуктов')
button_about = KeyboardButton(text='О нас')
kb.add(button_catalog, button_about)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Мы продаем продукты для Вашего здоровья:", reply_markup=kb)

@dp.message_handler(text='Перейти в каталог продуктов')
async def get_buying_list(message: types.Message):
    products = get_all_products()
    if products:
        for product in products:
            title, description, price = product[1], product[2], product[3]
            # Отправка фото если оно есть
            photo_path = os.path.join('files', f"{title.lower()}.jpg")  # Убедитесь, что названия файлов совпадают с названиями продуктов
            if os.path.exists(photo_path):
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=open(photo_path, 'rb'),
                    caption=f"Название: {title}\nОписание: {description}\nЦена: {price}"
                )
            else:
                await message.answer(f"Название: {title}\nОписание: {description}\nЦена: {price}\n(Фото нет)")
    else:
        await message.reply("Нет доступных продуктов.")

@dp.message_handler(text='О нас')
async def inform_about_us(message):
    await message.answer('Мы продаем только натуральные продукты')

@dp.message_handler()  # Общий обработчик
async def all_message(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)