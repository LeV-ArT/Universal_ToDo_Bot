import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
import openai
import aiohttp

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

async def ask_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150,
    )
    return response.choices[0].message['content']

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: Message):
    await message.answer("Думаю...")
    try:
        reply = await ask_gpt(message.text)
        await message.answer(reply)
    except Exception as e:
        await message.answer("Відбулася помилка при Вашому запиті.")
        print(f"Error: {e}")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: Message):
    await message.answear(f"Отримано фото: {message.photo[-1].file_id}")
    
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: Message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    await message.answer(f"Отримано документ: {file_name} (ID: {file_id})")

@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Запитати АІ", callback_data="ask_ai"),
        InlineKeyboardButton("Отримати фото", callback_data="get_photo"),
        InlineKeyboardButton("Отримати документ", callback_data="get_document")
    )
    await message.answer("Вітаю! Я бот, який може допомогти вам з різними запитами. Виберіть опцію:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'ask_ai')
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == 'ask_ai':
        await bot.send_message(callback_query.from_user.id, "Введіть запит до АІ:")
    elif data == 'get_photo':
        await bot.send_message(callback_query.from_user.id, "Надішліть фото, яке ви хочете обробити.")
    elif data == 'get_document':
        await bot.send_message(callback_query.from_user.id, "Надішліть документ, який ви хочете обробити.")
    await bot.answer_callback_query(callback_query.id)
