from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
 
def get_command_texts(lang: str = "ua") -> dict: 
    texts = { 
        "ua": { 
            "add": "➕ Додати завдання", 
            "list": "📋 Список Завдань", 
            "done": "✅ Позначити як виконане", 
            "delete": "🗑 Видалити завдання за ID", 
            "clear_done": "🧹 Очистити виконані завдання", 
            "delete_all": "🗑 Видалити Всі Завдання", 
            "cancel": "❌ Скасувати" 
        }, 
        "en": { 
            "add": "➕ Add Task", 
            "list": "📋 Task List", 
            "done": "✅ Mark as Done", 
            "delete": "🗑 Delete Task by ID", 
            "clear_done": "🧹 Clear Done Tasks", 
            "delete_all": "🗑 Delete All Tasks", 
            "cancel": "❌ Cancel" 
        }, 
        "ru": { 
            "add": "➕ Добавить задачу", 
            "list": "📋 Список задач", 
            "done": "✅ Отметить как выполненную", 
            "delete": "🗑 Удалить задачу по ID", 
            "clear_done": "🧹 Очистить выполненные задачи", 
            "delete_all": "🗑 Удалить все задачи", 
            "cancel": "❌ Отмена" 
        } 
    } 
    return texts.get(lang, texts["ua"]) 
 
 
def main_menu_keyboard(lang: str = "ua") -> ReplyKeyboardMarkup: 
    t = get_command_texts(lang) 
    return ReplyKeyboardMarkup( 
        keyboard=[ 
            [KeyboardButton(text=t["add"])], 
            [KeyboardButton(text=t["list"])], 
            [KeyboardButton(text=t["done"]), KeyboardButton(text=t["delete"])], 
            [KeyboardButton(text=t["clear_done"]), KeyboardButton(text=t["delete_all"])], 
            [KeyboardButton(text="⏰ Встановити дедлайн")],
            [KeyboardButton(text=t["cancel"])], 
        ], 
        resize_keyboard=True 
    )
