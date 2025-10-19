import json
from typing import Literal, List, TypedDict
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser, Namespace

DB = Path("./task_list.json")
TASK_STATUS = Literal["todo", "in-progress", "done"]


class Task(TypedDict):
    id: int
    description: str
    status: TASK_STATUS
    createdAt: datetime
    updatedAt: datetime


# Database
def load_database():
    try:
        if not DB.exists():
            print("Database does not exist, initializing...")
            return []
        else:
            return json.loads(DB.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_task_to_databse(tasks: List[Task]):
    DB.write_text(json.dumps(tasks, indent=4))


def find_by_id(tasks: List[Task], task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        else:
            print("Task not found")


def find_next_id(tasks: List[Task]):
    return max((task["id"] for task in tasks), default=0) + 1


# Commands
def task_add(args: Namespace):
    tasks = load_database()

    t: Task = {
        "id": find_next_id(tasks),
        "description": args.description,
        "status": "todo",
        "createdAt": str(datetime.now()),
        "updatedAt": str(datetime.now()),
    }

    tasks.append(t)
    save_task_to_databse(tasks)
    print(f"Task {t['id']} successfully added to list.\n {t}")


def task_update(args: Namespace, task_id: int):
    tasks = load_database()
    task = find_by_id(tasks, task_id)
    if not task:
        raise SystemExit(f"No task found with ID: {task_id}")

    task["description"] = args.description
    save_task_to_databse(tasks)
    print(f"Task {task[id]} description successfully updated.")


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Just another task tracker")
    sub = p.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Command to add a task")
    p_add.add_argument("description")
    p_add.set_defaults(func=task_add)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
