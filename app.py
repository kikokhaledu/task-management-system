from datetime import datetime
from typing import List, Union, Tuple

from flask import Flask, request, jsonify, make_response, abort

from constants import ALLOWED_STATUSES, ALLOWED_PRIORITIES
from db import (get_all_tasks, get_task, create_task, update_task, delete_task, filter_tasks,
                check_valid_status, check_valid_priority)
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/tasks', methods=['GET'])
def get_tasks() -> List[dict]:
    status = request.args.get('status')
    priority = request.args.get('priority')

    if status and status not in ALLOWED_STATUSES:
        return jsonify({"error": f"Invalid status value: {status}. Allowed values are {ALLOWED_STATUSES}"}), 400

    if priority and priority not in ALLOWED_PRIORITIES:
        return jsonify({"error": f"Invalid priority value: {priority}. Allowed values are {ALLOWED_PRIORITIES}"}), 400

    if status and priority:
        tasks = filter_tasks(status, priority)
    elif status:
        tasks = filter_tasks(status=status)
    elif priority:
        tasks = filter_tasks(priority=priority)
    else:
        tasks = get_all_tasks()

    return jsonify([task.serialize() for task in tasks])



@app.route('/tasks', methods=['POST'])
def post_task() -> Union[str, Tuple[str, int]]:
    """
    Create a new task with the provided data from the request JSON.

    :return: JSON representation of the created task and the HTTP status code.
    :raises BadRequest: If the request JSON is missing or any of the fields are not in the correct format.
    """
    if not request.json:
        abort(400)

    try:
        task = create_task(request.json)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(task.serialize()), 201



@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id: int) -> Union[str, Tuple[str, int]]:
    """Get a single task by its id."""
    task = get_task(task_id)
    if not task:
        abort(404)

    return jsonify(task.serialize())


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> Union[str, Tuple[str, int]]:
    """
    Update an existing task.

    :param task_id: The ID of the task to update.
    :return: A JSON object containing the updated task, or an error message with the corresponding status code.
    """
    task = get_task(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    task_data = request.get_json()

    if 'title' in task_data:
        task.title = task_data['title']

    if 'description' in task_data:
        task.description = task_data['description']

    if 'status' in task_data:
        status = task_data['status']
        if not check_valid_status(status):
            return jsonify({"error": f"Invalid status value: {status}. Allowed values are {ALLOWED_STATUSES}"}), 400
        task.status = status

    if 'priority' in task_data:
        priority = task_data['priority']
        if not check_valid_priority(priority):
            return jsonify({"error": f"Invalid priority value: {priority}. Allowed values are {ALLOWED_PRIORITIES}"}), 400
        task.priority = priority

    if 'due_date' in task_data:
        try:
            task.due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Expected format is 'YYYY-MM-DD'."}), 400

    db.session.commit()

    return jsonify(task.to_dict()), 200




@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_single_task(task_id: int) -> Union[str, Tuple[str, int]]:
    """Delete a task by its id."""
    task = get_task(task_id)
    if not task:
        abort(404)

    delete_task(task)
    return jsonify({"result": "Task deleted"})


@app.errorhandler(404)
def not_found(error: Exception) -> Tuple[str, int]:
    """Handle 404 errors."""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error: Exception) -> Tuple[str, int]:
    """Handle 400 errors."""
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
