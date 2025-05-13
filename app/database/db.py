from app.data.handler import get_tasks, save_all_tasks
def add_task(user_id: int, text: str):
    tasks = get_tasks()
    task_id = len(tasks) + 1
    tasks.append({
        "id": task_id,
        "user_id": user_id,
        "title": text,
        "description": "",
        "deadline": "",
        "done": False
    })
    save_all_tasks(tasks)
    return task_id

def get_all_tasks(user_id: int):
    return [task for task in get_tasks() if task["user_id"] == user_id]

def mark_task_done(user_id: int, task_id: int) -> bool:
    tasks = get_tasks()
    for task in tasks:
        if task["user_id"] == user_id and task["id"] == task_id:
            task["done"] = True
            save_all_tasks(tasks)
            return True
    return False

def delete_task_by_id(user_id: int, task_id: int) -> bool:
    tasks = get_tasks()
    updated_tasks = [task for task in tasks if not (task["user_id"] == user_id and task["id"] == task_id)]
    if len(tasks) == len(updated_tasks):
        return False  # Нічого не видалено
    save_all_tasks(updated_tasks)
    return True

def clear_done_tasks(user_id: int) -> int:
    tasks = get_tasks()
    new_tasks = [t for t in tasks if not (t["user_id"] == user_id and t["done"])]
    removed = len(tasks) - len(new_tasks)
    save_all_tasks(new_tasks)
    return removed

def delete_all_tasks(user_id: int) -> int:
    tasks = get_tasks()
    remaining_tasks = [t for t in tasks if t["user_id"] != user_id]
    deleted_count = len(tasks) - len(remaining_tasks)
    save_all_tasks(remaining_tasks)
    return deleted_count
