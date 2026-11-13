import os
import json

class Task:
    def __init__(self, title, description, completed):
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "Task Completed" if self.completed else "Task Pending"
        return f"Task: {self.title}\nDescription: {self.description}\nStatus: {status}"
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }