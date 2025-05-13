from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def language_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇦 Українська"), KeyboardButton(text="🇷🇺 Русский")],
            [KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )