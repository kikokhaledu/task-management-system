import unittest
import json
from app import app, db
from models import Task

with app.app_context():
    db.create_all()


class TestApp(unittest.TestCase):
    """
    Test suite for the task management application API endpoints.
    
    This class contains test cases for the CRUD operations on tasks and
    ensures the application's API is functioning as expected.
    """
    created_task_ids = []
    
    def setUp(self):
        self.client = app.test_client()

    def create_task(self, task_data):
        response = self.client.post('/tasks', data=json.dumps(task_data), content_type='application/json')
        task = json.loads(response.data)
        self.created_task_ids.append(task['id'])
        return task

    def tearDown(self):
        with app.app_context():
            for task_id in self.created_task_ids:
                task = db.session.get(Task, task_id)
                if task:
                    db.session.delete(task)
                    db.session.commit()
            self.created_task_ids.clear()


    def test_get_tasks(self):
        """Test retrieving all tasks."""
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_post_task(self):
        """Test creating a new task."""
        task_data = {
            'title': 'Another Test Task',
            'description': 'This is another test task',
            'status': 'not started',
            'priority': 'medium',
            'due_date': '2023-05-10'
        }
        response = self.client.post('/tasks', data=json.dumps(task_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        task = json.loads(response.data)
        self.created_task_ids.append(task['id'])

    def test_get_single_task(self):
        """Test retrieving a single task by ID."""
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'not started',
            'priority': 'medium',
            'due_date': '2023-05-10'
        }
        created_task = self.create_task(task_data)
        task_id = created_task["id"]

        response = self.client.get(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)

        retrieved_task = json.loads(response.data)
        self.assertEqual(retrieved_task["title"], created_task["title"])

    def test_update_task(self):
        """Test updating a task by ID."""
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'not started',
            'priority': 'medium',
            'due_date': '2023-05-10'
        }
        created_task = self.create_task(task_data)
        task_id = created_task["id"]

        updated_data = {
            'title': 'Updated Task',
            'description': 'This task has been updated',
            'status': 'in progress',
            'priority': 'high',
            'due_date': '2023-05-10'
        }
        response = self.client.put(f'/tasks/{task_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_single_task(self):
        """Test deleting a task by ID."""
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'not started',
            'priority': 'medium',
            'due_date': '2023-05-10'
        }
        created_task = self.create_task(task_data)
        task_id = created_task["id"]

        response = self.client.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
