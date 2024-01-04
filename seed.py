import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_tracker.settings')
django.setup()

from tasks.models import Task

def create_task(name, description, estimate, state="Planned"):
    task = Task(name=name, description=description, estimate=estimate, state=state)
    task.save()

with open('data/tasks.json', 'r') as f:
    data = json.load(f)
    for item in data:
        create_task(item['name'], item['description'], item['estimate'], item['state'])
