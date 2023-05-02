from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    """
    A class representing a task in the task management system.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(255), nullable=False, default='not started')
    priority = db.Column(db.String(255), nullable=False, default='medium')
    due_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, title, description, status, priority, due_date):
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.strftime('%Y-%m-%d') if self.due_date else None
        }