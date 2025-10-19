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
    createdAt: str
    updatedAt: str


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


# Helpers
def find_by_id(tasks: List[Task], task_id: int):
    for task in tasks:
        try:
            if task["id"] == task_id:
                return task
        except Exception as e:
            return f"Task with {task_id} not found..."


def find_next_id(tasks: List[Task]):
    return max((task["id"] for task in tasks), default=0) + 1


# Commands
def task_add(args: Namespace):
    tasks = load_database()

    date = datetime.now()

    task: Task = {
        "id": find_next_id(tasks),
        "description": args.description,
        "status": "todo",
        "createdAt": date.strftime("%A, %d. %B %Y %I:%M%p"),
        "updatedAt": date.strftime("%A, %d. %B %Y %I:%M%p"),
    }

    tasks.append(task)
    save_task_to_databse(tasks)
    print(f"Task {task['id']} successfully added to list.\n\n")

    print(f"{'ID':<4} {'STATUS':<12} {'CREATED AT':<20} {'UPDATED AT':<20} DESCRIPTION")
    print(
        f"{task['id']:<4} {task['status']:<12} {task['createdAt']:<20} {task['updatedAt']:<20} {task['description']}"
    )


def task_update(args: Namespace) -> None:
    tasks = load_database()
    task = find_by_id(tasks, args.id)
    if not task:
        raise SystemExit(f"No task found with ID: {args.id}")

    task["description"] = args.description
    save_task_to_databse(tasks)
    print(f"Task {task['id']} description successfully updated.\n\n")

    print(f"{'ID':<4} {'STATUS':<12} {'CREATED AT':<20} {'UPDATED AT':<20} DESCRIPTION")
    print(
        f"{task['id']:<4} {task['status']:<12} {task['createdAt']:<20} {task['updatedAt']:<20} {task['description']}"
    )


def task_delete(args: Namespace) -> None:
    tasks = load_database()

    before = len(tasks)
    tasks = [task for task in tasks if task["id"] != args.id]

    if len(tasks) == before:
        raise SystemExit(f"No task found with ID: {args.id}")
    save_task_to_databse(tasks)
    print(f"Task {args.id} successfully deleted")


def task_mark_in_progress(args: Namespace) -> None:
    tasks = load_database()

    task = find_by_id(tasks, args.id)
    if not task:
        raise SystemExit(f"No task found with ID: {args.id}")

    task["status"] = "in-progress"
    save_task_to_databse(tasks)


def task_mark_done(args: Namespace) -> None:
    tasks = load_database()
    task = find_by_id(tasks, args.id)

    if not task:
        raise SystemExit(f"No task found with ID: {args.id}")

    task["status"] = "done"
    save_task_to_databse(tasks)


def task_list(args: Namespace) -> None:
    tasks = load_database()
    valid_statuses = ["done", "in-progress", "all", "todo"]

    status = args.status
    if status not in valid_statuses:
        raise SystemExit(f"Invalid status, choose from {', '.join(valid_statuses)}")
    filtered = (
        tasks
        if status == "all"
        else [task for task in tasks if task["status"] == status]
    )

    if not filtered:
        raise SystemExit("No tasks")

    print(f"{'ID':<4} {'STATUS':<12} {'CREATED AT':<20} {'UPDATED AT':<20} DESCRIPTION")
    for task in sorted(filtered, key=lambda x: x["id"]):
        print(
            f"{task['id']:<4} {task['status']:<12} {task['createdAt']:<20} {task['updatedAt']:<20} {task['description']}"
        )


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Just another task tracker")
    sub = p.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Command to add a task")
    p_add.add_argument("description")
    p_add.set_defaults(func=task_add)

    p_update = sub.add_parser("update", help="Command to delete a task")
    p_update.add_argument("id", type=int)
    p_update.add_argument("description")
    p_update.set_defaults(func=task_update)

    p_delete = sub.add_parser("delete", help="Command to delete a task")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=task_delete)

    p_mark_in_progress = sub.add_parser(
        "mark-in-progress", help="Command to mark a task in progress"
    )
    p_mark_in_progress.add_argument("id", type=int)
    p_mark_in_progress.set_defaults(func=task_mark_in_progress)

    p_mark_done = sub.add_parser("mark-done", help="Command to mark a task done")
    p_mark_done.add_argument("id", type=int)
    p_mark_done.set_defaults(func=task_mark_done)

    p_list_tasks = sub.add_parser("list", help="Command to list tasks")
    p_list_tasks.add_argument("status", nargs="?", default="all")
    p_list_tasks.set_defaults(func=task_list)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
