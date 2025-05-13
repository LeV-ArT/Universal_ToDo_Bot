from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def task_list_keyboard(tasks):
    keyboard = InlineKeyboardMarkup()
    for i, task in enumerate(tasks, start=1):
        button = InlineKeyboardButton(
            text=f"{i}. {task['title']} ({task['creation_time']})",
            callback_data=f"view_task_{i - 1}"
        )
        keyboard.add(button)
    return keyboard

def task_details_keyboard(task_index):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✏️ Edit title", callback_data=f"edit_title_{task_index}"),
        InlineKeyboardButton("📝 Edit description", callback_data=f"edit_desc_{task_index}"),
    )
    keyboard.add(
        InlineKeyboardButton("📅 Edit deadline", callback_data=f"edit_deadline_{task_index}"),
        InlineKeyboardButton("🔁 Change status", callback_data=f"change_status_{task_index}"),
    )
    keyboard.add(
        InlineKeyboardButton("🗑 Delete task", callback_data=f"delete_task_{task_index}")
    )
    return keyboard
