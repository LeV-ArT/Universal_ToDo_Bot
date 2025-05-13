from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.fsm.language import LangState
from app.keyboards.language import language_keyboard
from app.keyboards.menu import main_menu_keyboard

from app.data.handler import load_user_data

user_languages = {}

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("🌐 Виберіть мову / Choose your language:", reply_markup=language_keyboard())
    await state.set_state(LangState.choosing_language)

@router.message(LangState.choosing_language)
async def set_language(message: Message, state: FSMContext):
    lang_map = {
        "🇺🇦 Українська": "ua",
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en"
    }
    selected_lang = lang_map.get(message.text)
    if not selected_lang:
        await message.answer("❗️ Будь ласка, оберіть мову з клавіатури.")
        return

    user_languages[message.from_user.id] = selected_lang
    await state.clear()
    
    await message.answer("✅ Мову збережено!", reply_markup=main_menu_keyboard(selected_lang))

def get_user_language(user_id: int) -> str:
    if user_id in user_languages:
        return user_languages[user_id]

    user_data = load_user_data()
    lang = user_data.get(str(user_id), "ua")
    user_languages[user_id] = lang
    return lang
