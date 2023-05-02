from typing import List, Optional, Dict, Union
from models import Task, db
from datetime import datetime
from constants import ALLOWED_STATUSES, ALLOWED_PRIORITIES


def get_all_tasks() -> List[Task]:
    """Return a list of all tasks."""
    return Task.query.all()


def get_task(task_id: int) -> Optional[Task]:
    """Return a task with the given task_id, or None if not found."""
    return db.session.get(Task, task_id)





def create_task(task_data: Dict[str, any]) -> Task:
    """
    Create a new task with the provided data.

    :param task_data: A dictionary containing the task data.
    :return: The created Task object.
    :raises ValueError: If any of the fields are not in the correct format.
    """
    if 'title' not in task_data or not task_data['title']:
        raise ValueError("Title is required")

    if 'status' in task_data and task_data['status'] not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status value: {task_data['status']}. Allowed values are {ALLOWED_STATUSES}")

    if 'priority' in task_data and task_data['priority'] not in ALLOWED_PRIORITIES:
        raise ValueError(f"Invalid priority value: {task_data['priority']}. Allowed values are {ALLOWED_PRIORITIES}")

    due_date = task_data.get('due_date', None)
    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid due_date format. Expected format: 'YYYY-MM-DD'")

    status = task_data.get('status', 'not started')
    priority = task_data.get('priority', 'medium')

    task = Task(
        title=task_data['title'],
        description=task_data.get('description', None),
        status=status,
        priority=priority,
        due_date=due_date
    )
    db.session.add(task)
    db.session.commit()
    return task



def update_task(task_id: int, task_data: Dict[str, Union[str, Optional[str]]]) -> Optional[Task]:
    """Update a task with the given task_id and task_data, and return the updated task, or None if not found."""
    task = Task.query.get(task_id)

    if not task:
        return None

    if 'title' in task_data:
        task.title = task_data['title']

    if 'description' in task_data:
        task.description = task_data['description']

    if 'status' in task_data:
        status = task_data['status']
        if not check_valid_status(status):
            raise ValueError(f"Invalid status value: {status}. Allowed values are {ALLOWED_STATUSES}")
        task.status = status

    if 'priority' in task_data:
        priority = task_data['priority']
        if not check_valid_priority(priority):
            raise ValueError(f"Invalid priority value: {priority}. Allowed values are {ALLOWED_PRIORITIES}")
        task.priority = priority

    if 'due_date' in task_data:
        try:
            task.due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid due_date format. Expected format is 'YYYY-MM-DD'.")

    db.session.commit()
    return task



def delete_task(task: Task) -> None:
    """Delete the given task."""
    db.session.delete(task)
    db.session.commit()


def filter_tasks(status: Optional[str] = None, priority: Optional[str] = None) -> List[Task]:
    """Filter tasks by the given status and/or priority and return a list of tasks."""
    query = Task.query
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    return query.all()

def check_valid_status(status: str) -> bool:
    """Check if the given status is valid."""
    return status in ALLOWED_STATUSES


def check_valid_priority(priority: str) -> bool:
    """Check if the given priority is valid."""
    return priority in ALLOWED_PRIORITIES
