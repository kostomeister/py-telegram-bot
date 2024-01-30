import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from openai import OpenAI
from dotenv import load_dotenv

from db_handler.db_handler import db
from utils.chat_openai import get_chat_report
from utils.keyboard import (
    locations_keyboard,
    checklist_keyboard,
    report_keyboard,
    photo_keyboard,
)
from photo_handler.photo_handler import photo_handler

load_dotenv()

# Встановлення токенів для Telegram бота та OpenAI
BOT_TOKEN = os.getenv("BOT_TOKEN")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


# Визначення станів
class BotState(StatesGroup):
    Location = State()  # Стан для вибору локації
    Checklist = State()  # Стан для вибору стану локації
    Comment = State()  # Стан для введення коментаря (в разі вибору "Залишити коментар")
    PhotoDecision = State()  # Стан для вибору користувачем, чи він хоче додати фото
    WaitingForPhoto = State()  # Стан для очікування фото


# Обробник команди /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(
        "Привіт! Я твій бот. Напиши '/send_report', щоб розпочати.",
        reply_markup=report_keyboard,
    )


# Обробник команди send_report
@dp.message_handler(commands=["send_report"])
async def send_report_command(message: types.Message):
    await message.answer("Обери локацію:", reply_markup=locations_keyboard)

    # Задаємо початковий стан - вибір локації
    await BotState.Location.set()


# Обробник вибору локації
@dp.message_handler(state=BotState.Location)
async def location_selected(message: types.Message, state: FSMContext):
    user_data = {"location": message.text}
    await state.update_data(user_data)
    await message.answer("Обери стан локації:", reply_markup=checklist_keyboard)

    # Очікування вибору стану локації перед реєстрацією обробників для коментаря чи фото
    await BotState.Checklist.set()


# Обробник вибору стану локації
@dp.message_handler(state=BotState.Checklist)
async def checklist_selected(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_data["checklist"] = message.text

    if message.text == "Залишити коментар":
        await message.answer("Введи коментар:")

        # Скасування попереднього очікування стану та реєстрація обробника для коментаря
        await state.update_data(user_data)
        await BotState.Comment.set()

    else:
        await message.answer("Дякую за відгук! Звіт буде проаналізовано.")
        await create_ai_report(message, user_data)

        # Скидання стану
        await state.finish()


# Обробник введення коментаря
@dp.message_handler(state=BotState.Comment)
async def comment_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_data["comment"] = message.text

    # Питання користувачу, чи він хоче надіслати фото

    await message.answer("Чи хочеш додати фото?", reply_markup=photo_keyboard)

    # Збереження коментаря у стані
    await state.update_data(user_data)
    # Очікування вибору користувачем, чи він хоче додати фото
    await BotState.PhotoDecision.set()


async def create_ai_report(message: types.Message, user_data: dict):
    # Перевірка чи існує репорт в базі даних від цього користувача для цієї локації
    existing_reports = db.get_existing_reports(
        user_id=message.from_user.id, location=user_data["location"]
    )

    # Формування звіту
    report = (
        f"Локація: {user_data['location']}\n"
        f"Стан: {user_data['checklist']}\n"
        f"Коментар: {user_data.get('comment', 'Немає коментаря')}\n"
    )

    context_reports = None
    if existing_reports:
        # Якщо є репорт, використовуйте його як контекст для OpenAI
        context_reports = "\n".join([report["comment"] for report in existing_reports])

    openai_response = get_chat_report(client, report, context_reports)

    # Зберігання даних у базі даних
    db.insert_report(**user_data, user_id=message.from_user.id)

    # Скидання стану обробника
    await dp.storage.reset_data(chat=message.chat.id, user=message.from_user.id)
    await message.answer(f"Аналіз від штучного інтелекту: {openai_response}")
    await message.answer(
        "Щоб створити новий звіт надішліть /send_report", reply_markup=report_keyboard
    )


# Обробник введення користувачем, чи він хоче додати фото
@dp.message_handler(state=BotState.PhotoDecision)
async def photo_decision(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    if message.text == "Додати фото":
        # Якщо користувач обрав "Додати фото", очікуємо фото
        await message.answer("Тепер надішли фото.")
        await BotState.WaitingForPhoto.set()
    elif message.text == "Пропустити":
        # Якщо користувач пропустив додавання фото, викликаємо функцію для створення звіту від AI
        await message.answer("Дякую за відгук! Звіт буде проаналізовано.")
        await create_ai_report(message, user_data)
        # Скидання стану
        await state.finish()
    else:
        await message.answer(
            "Будь ласка, обери один з варіантів:", reply_markup=photo_keyboard
        )


# Обробник введення фото
@dp.message_handler(
    state=BotState.WaitingForPhoto, content_types=types.ContentType.PHOTO
)
async def photo_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    if message.photo:
        # Якщо користувач відправив фото, перевіряємо його розмір
        if (
            message.photo[-1].file_size <= 5 * 1024 * 1024
        ):  # Перевірка розміру файлу (менше 5 МБ)
            # Зберігаємо фото та встановлюємо фото URL у user_data
            photo_file_id = await photo_handler.save_photo_data(message, bot=bot)
            user_data["photo_url"] = photo_file_id

            # Відправка повідомлення про завершення та визов функції для створення звіту від AI
            await message.answer("Дякую за відгук! Звіт буде проаналізовано.")
            await create_ai_report(message, user_data)

            # Скидання стану
            await state.finish()
        else:
            # Якщо фото завелике, повідомте користувача і дайте йому ще одну спробу
            await message.answer(
                "Розмір фото перевищує 5 МБ. Спробуйте надіслати інше фото."
            )
    else:
        # Якщо користувач надіслав не фото, повідомте його про помилку
        await message.answer("Будь ласка, надішліть фото.")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
