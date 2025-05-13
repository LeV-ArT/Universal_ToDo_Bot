import os 
import json 
 
def ensure_file_exists(f_path: str = "data/tasks.json"):
    os.makedirs(os.path.dirname(f_path), exist_ok=True)
    if not os.path.isfile(f_path):
        with open(f_path, "w") as f:
            json.dump({"tasks": []}, f)

def get_tasks(f_path: str = "data/tasks.json") -> list:
    ensure_file_exists(f_path)
    with open(f_path) as f:
        data = json.load(f)
        tasks = data.get("tasks", [])
        return tasks

def get_task(id: int = 0, f_path: str = "data/tasks.json") -> dict:
    tasks = get_tasks(f_path)
    return tasks[id]

def save_task(task: dict = {}, f_path: str = "data/tasks.json") -> bool:
    ensure_file_exists(f_path)
    with open(f_path) as f:
        data = json.load(f)
        tasks = data.get("tasks", [])
        tasks.append(task)
        data["tasks"] = tasks
    with open(f_path, "w") as f:
        json.dump(data, f, indent=4)
    return True

def save_all_tasks(tasks: list, f_path: str = "data/tasks.json") -> bool:
    ensure_file_exists(f_path)
    data = {"tasks": tasks}
    with open(f_path, "w") as f:
        json.dump(data, f, indent=4)
    return True



def load_user_data():
    if not os.path.exists("app/data/user_data.json"):
        return {}
    with open("app/data/user_data.json", "r") as f:
        return json.load(f)


def save_user_data(data):
    with open("app/data/user_data.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    print(get_tasks())
