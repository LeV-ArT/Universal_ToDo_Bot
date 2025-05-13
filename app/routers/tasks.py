from aiogram import Router, F, types 
from aiogram.fsm.context import FSMContext 
from aiogram.fsm.state import State, StatesGroup 
from aiogram.types import ReplyKeyboardRemove, Message 
import datetime
from aiogram import Bot

from app.data.handler import get_tasks, save_all_tasks
from app.keyboards.menu import main_menu_keyboard 
from app.database.db import ( 
    add_task, get_all_tasks, mark_task_done, 
    delete_task_by_id, clear_done_tasks, delete_all_tasks 
) 
from app.routers.language import user_languages 
 
import re 

router = Router() 
 
class TaskState(StatesGroup): 
    waiting_for_task = State()

def get_user_lang(msg: types.Message) -> str: 
    return user_languages.get(msg.from_user.id, "ua") 
 
def get_command_texts(lang: str) -> dict: 
    return { 
        "Add Task": { 
            "ua": "➕ Додати завдання", 
            "en": "➕ Add Task", 
            "ru": "➕ Добавить задачу" 
        }, 
        "List Tasks": { 
            "ua": "📋 Список Завдань", 
            "en": "📋 Task List", 
            "ru": "📋 Список задач" 
        }, 
        "Mark as Done": { 
            "ua": "✅ Позначити як виконане", 
            "en": "✅ Mark as Done", 
            "ru": "✅ Отметить как выполненное" 
        }, 
        "Delete by ID": { 
            "ua": "🗑 Видалити завдання за ID", 
            "en": "🗑 Delete Task by ID", 
            "ru": "🗑 Удалить задачу по ID" 
        }, 
        "Clear Done": { 
            "ua": "🧹 Очистити виконані завдання", 
            "en": "🧹 Clear Done Tasks", 
            "ru": "🧹 Очистить выполненные задачи" 
        }, 
        "Delete All": { 
            "ua": "🗑 Видалити Всі Завдання", 
            "en": "🗑 Delete All Tasks", 
            "ru": "🗑 Удалить все задачи" 
        }, 
        "Cancel": { 
            "ua": "❌ Скасувати", 
            "en": "❌ Cancel", 
            "ru": "❌ Отмена" 
        } 
    } 
 
def get_text(key: str, lang: str) -> str: 
    texts = { 
        "start": { 
            "ua": "👋 Вітаєм вас у Task Manager Bot!\nВиберіть один з варіантів дії:", 
            "en": "👋 Welcome to Task Manager Bot!\nChoose an action:", 
            "ru": "👋 Добро пожаловать в Task Manager Bot!\nВыберите действие:" 
        }, 
        "enter_task": { 
            "ua": "📝 Будь ласка, введіть своє завдання:", 
            "en": "📝 Please enter your task:", 
            "ru": "📝 Пожалуйста, введите задачу:" 
        }, 
        "task_added": { 
            "ua": "✅ Завдання успішно додане!", 
            "en": "✅ Task added successfully!", 
            "ru": "✅ Задача успешно добавлена!" 
        }, 
        "no_tasks": { 
            "ua": "🕳 Завдань не знайдено.", 
            "en": "🕳 No tasks found.", 
            "ru": "🕳 Задачи не найдены." 
        }, 
        "task_list_title": { 
            "ua": "📝 Ваші завдання:", 
            "en": "📝 Your tasks:", 
            "ru": "📝 Ваши задачи:" 
        }, 
        "cancelled": { 
            "ua": "❌ Скасовано", 
            "en": "❌ Cancelled", 
            "ru": "❌ Отменено" 
        }, 
        "enter_done_format": { 
            "ua": "✅ Введи команду у форматі:\nDone 1", 
            "en": "✅ Enter the command in the format:\nDone 1", 
            "ru": "✅ Введите команду в формате:\nDone 1" 
        }, 
        "task_marked": { 
            "ua": "✅ Задачу позначено як виконану.", 
            "en": "✅ Task marked as done.", 
            "ru": "✅ Задача отмечена как выполненная." 
        }, 
        "task_not_found": { 
            "ua": "❌ Задачу не знайдено.", 
            "en": "❌ Task not found.", 
            "ru": "❌ Задача не найдена." 
        }, 
        "wrong_format": { 
            "ua": "❌ Неправильний формат. Приклад: Done 2", 
            "en": "❌ Incorrect format. Example: Done 2", 
            "ru": "❌ Неверный формат. Пример: Done 2" 
        }, 
        "enter_delete_format": { 
            "ua": "🗑 Введи команду у форматі:\nDelete 1", 
            "en": "🗑 Enter the command in the format:\nDelete 1", 
            "ru": "🗑 Введите команду в формате:\nDelete 1" 
        }, 
        "task_deleted": { 
            "ua": "🗑 Задача з ID {id} видалена.", 
            "en": "🗑 Task with ID {id} deleted.", 
            "ru": "🗑 Задача с ID {id} удалена." 
        }, 
        "task_not_deleted": { 
            "ua": "⚠️ Задача з ID {id} не знайдена.", 
            "en": "⚠️ Task with ID {id} not found.", 
            "ru": "⚠️ Задача с ID {id} не найдена." 
        }, 
        "cleared_done": { 
            "ua": "🧹 Видалено {count} виконаних задач.", 
            "en": "🧹 Cleared {count} completed tasks.", 
            "ru": "🧹 Удалено {count} выполненных задач."
}, 
        "all_deleted": { 
            "ua": "🗑 Видалено всі задачі ({count} шт.)", 
            "en": "🗑 Deleted all tasks ({count} items)", 
            "ru": "🗑 Удалены все задачи ({count} шт.)" 
        } 
    } 
    return texts.get(key, {}).get(lang, texts.get(key, {}).get("ua", "")) 
 
# 🔹 Додати завдання 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["Add Task"][get_user_lang(msg)]) 
async def add_task_start(message: types.Message, state: FSMContext): 
    lang = get_user_lang(message) 
    await message.answer(get_text("enter_task", lang), reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(TaskState.waiting_for_task) 
 
@router.message(TaskState.waiting_for_task) 
async def receive_task(message: types.Message, state: FSMContext): 
    lang = get_user_lang(message) 
    add_task(message.from_user.id, message.text) 
    await message.answer(get_text("task_added", lang), reply_markup=main_menu_keyboard(lang)) 
    await state.clear() 
 
# 🔹 Перегляд задач 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["List Tasks"][get_user_lang(msg)]) 
async def list_tasks(message: types.Message): 
    lang = get_user_lang(message) 
    tasks = get_all_tasks(message.from_user.id) 
 
    if not tasks: 
        await message.answer(get_text("no_tasks", lang)) 
        return 
 
    response = f"<b>{get_text('task_list_title', lang)}</b>\n" 
    for task in tasks: 
        status_icon = "✅" if task["done"] else "⏳" 
        response += f"\n<b>[{task['id']}] {task['title']}</b>\n" 
        if task["description"]: 
            response += f"🗒 {task['description']}\n" 
        if task["deadline"]: 
            response += f"⏰ Дедлайн: {task['deadline']}\n" 
        status_text = { 
            "ua": "Виконане" if task["done"] else "Не виконане", 
            "en": "Done" if task["done"] else "Not done", 
            "ru": "Выполнено" if task["done"] else "Не выполнено" 
        } 
        response += f"📌 Статус: {status_icon} {status_text.get(lang)}\n" 
 
    response += f"\n\n✏️ <b>Done 1</b> — {get_text('enter_done_format', lang).splitlines()[1]}" 
    response += f"\n🗑 <b>Delete 1</b> — {get_text('enter_delete_format', lang).splitlines()[1]}" 
    await message.answer(response, parse_mode="HTML") 
 
# 🔹 Скасувати 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["Cancel"][get_user_lang(msg)]) 
async def cancel(message: types.Message, state: FSMContext): 
    lang = get_user_lang(message) 
    await state.clear() 
    await message.answer(get_text("cancelled", lang), reply_markup=main_menu_keyboard(lang)) 
 
# 🔹 Позначити як виконане 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["Mark as Done"][get_user_lang(msg)]) 
async def prompt_mark_done(message: types.Message): 
    lang = get_user_lang(message) 
    await message.answer(get_text("enter_done_format", lang)) 
 
@router.message(lambda msg: msg.text.lower().startswith("✅ done") or msg.text.lower().startswith("done")) 
async def mark_done_handler(message: types.Message): 
    lang = get_user_lang(message) 
    try: 
        task_id = int(message.text.lower().replace("✅ done", "").replace("done", "").strip()) 
        if mark_task_done(message.from_user.id, task_id): 
            await message.answer(get_text("task_marked", lang)) 
        else: 
            await message.answer(get_text("task_not_found", lang)) 
    except ValueError: 
        await message.answer(get_text("wrong_format", lang)) 
 
# 🔹 Видалити завдання 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["Delete by ID"][get_user_lang(msg)]) 
async def prompt_delete_task(message: types.Message): 
    lang = get_user_lang(message) 
    await message.answer(get_text("enter_delete_format", lang)) 
 
@router.message(lambda msg: re.fullmatch(r"(🗑 )?delete \d+", msg.text.lower())) 
async def delete_task_handler(message: types.Message): 
    lang = get_user_lang(message) 
    try: 
        task_id = int(message.text.lower().split()[-1])
        if delete_task_by_id(message.from_user.id, task_id): 
            await message.answer(get_text("task_deleted", lang).format(id=task_id)) 
        else: 
            await message.answer(get_text("task_not_deleted", lang).format(id=task_id)) 
    except (IndexError, ValueError): 
        await message.answer(get_text("wrong_format", lang)) 
 
# 🔹 Очистити виконані 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["Clear Done"][get_user_lang(msg)]) 
async def clear_done_handler(message: Message): 
    lang = get_user_lang(message) 
    count = clear_done_tasks(message.from_user.id) 
    await message.answer(get_text("cleared_done", lang).format(count=count)) 
 
# 🔹 Видалити всі задачі 
@router.message(lambda msg: msg.text == get_command_texts(get_user_lang(msg))["Delete All"][get_user_lang(msg)]) 
async def delete_all_handler(message: types.Message): 
    lang = get_user_lang(message) 
    count = delete_all_tasks(message.from_user.id) 
    await message.answer(get_text("all_deleted", lang).format(count=count))

# 🔹 Встановити дедлайн
@router.message(lambda msg: msg.text == "⏰ Встановити дедлайн")
async def prompt_set_deadline(message: types.Message):
    lang = get_user_lang(message)
    await message.answer("⏰ Введіть команду у форматі:\nDeadline [ID] [DD/MM/YYYY HH:MM]")

@router.message(lambda msg: msg.text.lower().startswith("deadline"))
async def set_deadline_handler(message: types.Message):
    lang = get_user_lang(message)
    try:
        # Розділяємо текст на три частини: команда, ID задачі, дедлайн
        parts = message.text.split(maxsplit=2)
        if len(parts) != 3:
            raise ValueError("Invalid format")

        # Перевіряємо, чи ID задачі є числом
        try:
            task_id = int(parts[1])
        except ValueError:
            raise ValueError("Task ID must be a number")

        # Перевіряємо формат дати та часу
        try:
            deadline = datetime.datetime.strptime(parts[2], "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("Invalid date format")

        # Отримуємо всі задачі користувача
        tasks = get_all_tasks(message.from_user.id)
        for task in tasks:
            if task["id"] == task_id:
                # Оновлюємо дедлайн задачі
                task["deadline"] = deadline.strftime("%d/%m/%Y %H:%M")
                save_all_tasks(tasks)
                await message.answer(
                    f"✅ Дедлайн для задачі №{task_id} встановлено: {deadline.strftime('%d/%m/%Y %H:%M')}"
                )
                return

        # Якщо задача не знайдена
        await message.answer("❌ Задачу не знайдено.")
    except ValueError as e:
        # Відправляємо повідомлення про помилку
        await message.answer(f"❌ {str(e)}. Приклад: Deadline 1 25/12/2025 14:30")
        
# Перевірка дедлайнів
async def check_deadlines(bot: Bot):
    tasks = get_tasks()
    now = datetime.datetime.now()
    for task in tasks:
        if not task["done"] and task["deadline"]:
            deadline = datetime.datetime.strptime(task["deadline"], "%d/%m/%Y %H:%M")
            time_diff = deadline - now
            if 0 < time_diff.total_seconds() <= 3600:  # Якщо дедлайн через 1 годину
                await bot.send_message(
                    task["user_id"],
                    f"⏰ У вас встановлений дедлайн на сьогодні о {deadline.strftime('%H:%M')}!"
                )