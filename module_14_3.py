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


api = '7896102855:AAHI1_Ozmi5PdqWVy9arpb1jibnmxwbFK9g'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button_1 = KeyboardButton(text = 'Информация')
button_2 = KeyboardButton(text = 'Рассчитать')
button_3 = KeyboardButton(text = 'Купить')
kb.row(button_1, button_2, button_3)



kb1 = InlineKeyboardMarkup()
button_4 = InlineKeyboardButton('Рассчитать норму калорий', callback_data = 'calories')
button_5 = InlineKeyboardButton('Формулы расчета', callback_data = 'formulas')
kb1.add(button_4, button_5)


# kb_product = InlineKeyboardMarkup()
# button_pr1 = InlineKeyboardButton('Product1', callback_data = 'product_buying')
# button_pr2 = InlineKeyboardButton('Product2', callback_data = 'product_buying')
# button_pr3 = InlineKeyboardButton('Product3', callback_data = 'product_buying')
# button_pr4 = InlineKeyboardButton('Product4', callback_data = 'product_buying')
# kb_product.add(button_pr1, button_pr2, button_pr3, button_pr4)

kb_product = InlineKeyboardMarkup()
for i in range(1, 5):
    kb_product.add(InlineKeyboardButton(f'Product{i}', callback_data='product_buying'))


@dp.message_handler(text = "Купить")             # Обработчик для кнопки купить
async def get_buying_list(message):
    products_info = [
        ("Название: Product1 | Описание: описание 1 | Цена: 100", "files/product1.jpg"),
        ("Название: Product2 | Описание: описание 2 | Цена: 200", "files/product2.jpg"),
        ("Название: Product3 | Описание: описание 3 | Цена: 300", "files/product3.jpg"),
        ("Название: Product4 | Описание: описание 4 | Цена: 400", "files/product4.jpg"),
    ]

    for product, photo_path in products_info:
        # Отправляем фото
        with open(photo_path, 'rb') as photo:
            await message.answer_photo(photo, caption=product)

    # for product in products_info:
    #     await message.answer(product)
    await message.answer("Выберите продукт для покупки", reply_markup=kb_product)

@dp.callback_query_handler(text='product_buying')  # Новый обработчик для inline кнопок
async def send_confirm_message(call):
    await call.answer()  # Подтверждаем нажатие кнопки
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью:", reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb1)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Расчет нормы потребления калорий. Нажмите "Рассчитать"')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.message.answer('для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161:')
    await call.answer()

@dp.message_handler(text = 'Информация')
async def inform(message):
    await message.answer('Рекомендуемая норма потребления каллорий рассчитана по формуле Мифлина-Сан Жеора')

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer("Норма каллорий для Вас (для мужчин) "
    f"{10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5}")

@dp.message_handler()  # Мы получили сообщение
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)