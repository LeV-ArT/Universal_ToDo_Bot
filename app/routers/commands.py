from aiogram import Router, types
from aiogram.filters import Command
from app.database.db import mark_task_done, delete_task_by_id, clear_done_tasks

router = Router()

@router.message(Command("done"))
async def cmd_done(message: types.Message):
    try:
        task_id = int(message.text.split()[1])
        success = mark_task_done(message.from_user.id, task_id)
        if success:
            await message.answer(f"✅ Завдання №{task_id} позначено як виконане.")
        else:
            await message.answer("❗️ Завдання не знайдено.")
    except:
        await message.answer("❗️ Правильне використання: /done [id]")

@router.message(Command("delete"))
async def cmd_delete(message: types.Message):
    try:
        task_id = int(message.text.split()[1])
        success = delete_task_by_id(message.from_user.id, task_id)
        if success:
            await message.answer(f"🗑 Завдання №{task_id} видалено.")
        else:
            await message.answer("❗️ Завдання не знайдено.")
    except:
        await message.answer("❗️ Правильне використання: /delete [id]")

@router.message(Command("clear"))
async def cmd_clear(message: types.Message):
    count = clear_done_tasks(message.from_user.id)
    await message.answer(f"🧹 Видалено {count} виконаних завдань.")
