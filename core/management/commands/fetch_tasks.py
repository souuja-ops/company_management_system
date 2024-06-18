# core/management/commands/fetch_tasks.py

import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Task, Department, Employee

class Command(BaseCommand):
    help = 'Fetch tasks from JSON Placeholder API and populate the database'

    def handle(self, *args, **kwargs):
        # Create departments if they don't exist
        departments = ['HR', 'IT', 'Finance', 'Marketing']
        for dept_name in departments:
            Department.objects.get_or_create(name=dept_name)

        # Assign each user to a random department if they don't have one
        users = User.objects.all()
        for user in users:
            if not Employee.objects.filter(user=user).exists():
                department = Department.objects.order_by('?').first()  # Random department
                Employee.objects.create(user=user, department=department)

        # Fetch tasks from JSON Placeholder API
        response = requests.get('https://jsonplaceholder.typicode.com/todos')
        tasks = response.json()

        for task in tasks:
            user = User.objects.order_by('?').first()  # Assign to a random user
            Task.objects.create(
                title=task['title'],
                description='',
                assigned_to=user,
                completed=task['completed'],
            )

        self.stdout.write(self.style.SUCCESS('Successfully fetched and added tasks and departments.'))
