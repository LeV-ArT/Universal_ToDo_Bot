from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.routers.tasks import check_deadlines

from app.routers import language, tasks, commands  # усі імпорти в одному місці
from app.keyboards.menu import main_menu_keyboard

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не встановлено. Задай змінну середовища.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 💡 ВАЖЛИВО: language має бути першим
dp.include_router(language.router)
dp.include_router(tasks.router)
dp.include_router(commands.router)

async def on_startup():
    print("✅ Deleting webhook (if any)...")
    await bot.delete_webhook()  # Delete the webhook to enable polling

    # Ініціалізація планувальника
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_deadlines, "interval", minutes=1, args=[bot])  # Перевірка дедлайнів кожну хвилину
    scheduler.start()

    print("✅ Bot is running...")

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())