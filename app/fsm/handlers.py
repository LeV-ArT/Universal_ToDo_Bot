from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.data.handler import get_tasks, save_all_tasks
from .states import TaskEditStates



router = Router()

# --- Назва ---
@router.callback_query(F.data.startswith("edit_title_"))
async def start_edit_title(callback: types.CallbackQuery, state: FSMContext):
    task_index = int(callback.data.split("_")[-1])
    await state.set_state(TaskEditStates.waiting_for_title)
    await state.update_data(task_index=task_index)
    await callback.message.answer("✏️ Enter new task title:")
    await callback.answer()

@router.message(TaskEditStates.waiting_for_title)
async def process_edit_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_index = data["task_index"]
    tasks = get_tasks()
    tasks[task_index]["title"] = message.text
    save_all_tasks(tasks)
    await message.answer("✅ Title updated!")
    await state.clear()

# --- Опис ---
@router.callback_query(F.data.startswith("edit_desc_"))
async def start_edit_description(callback: types.CallbackQuery, state: FSMContext):
    task_index = int(callback.data.split("_")[-1])
    await state.set_state(TaskEditStates.waiting_for_description)
    await state.update_data(task_index=task_index)
    await callback.message.answer("📝 Enter new task description:")
    await callback.answer()

@router.message(TaskEditStates.waiting_for_description)
async def process_edit_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_index = data["task_index"]
    tasks = get_tasks()
    tasks[task_index]["description"] = message.text
    save_all_tasks(tasks)
    await message.answer("✅ Description updated!")
    await state.clear()

# --- Дедлайн ---
@router.callback_query(F.data.startswith("edit_deadline_"))
async def start_edit_deadline(callback: types.CallbackQuery, state: FSMContext):
    task_index = int(callback.data.split("_")[-1])
    await state.set_state(TaskEditStates.waiting_for_deadline)
    await state.update_data(task_index=task_index)
    await callback.message.answer("📅 Enter new deadline (DD/MM/YYYY):")
    await callback.answer()

@router.message(TaskEditStates.waiting_for_deadline)
async def process_edit_deadline(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%d/%m/%Y")
    except ValueError:
        await message.answer("⚠️ Invalid format! Use DD/MM/YYYY.")
        return

    data = await state.get_data()
    task_index = data["task_index"]
    tasks = get_tasks()
    tasks[task_index]["deadline"] = message.text
    save_all_tasks(tasks)
    await message.answer("✅ Deadline updated!")
    await state.clear()
