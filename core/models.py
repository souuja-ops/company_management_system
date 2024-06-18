from django.contrib.auth.models import User
from django.db import models

# Model for user roles
class Role(models.Model):
    # Choices for roles
    ROLE_CHOICES = [
        ('employee', 'Employee'),   # Role for regular employees
        ('manager', 'Manager'),     # Role for managers
        # Add more roles here as needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # Role field with predefined choices

    def __str__(self):
        return f"{self.user.username} - {self.role}"  # String representation of Role instance, showing username and role


# Model for departments
class Department(models.Model):
    name = models.CharField(max_length=100)  # Name field for department

    def __str__(self):
        return self.name  # String representation of Department instance, showing department name


# Model for tasks
class Task(models.Model):
    title = models.CharField(max_length=255)  # Title field for task
    description = models.TextField()  # Description field for task
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model for task assignment
    completed = models.BooleanField(default=False)  # Boolean field to track task completion status
    created_at = models.DateTimeField(auto_now_add=True)  # DateTime field to store task creation timestamp

    def __str__(self):
        return self.title  # String representation of Task instance, showing task title


# Model for employees
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User model
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # ForeignKey to Department model for employee's department

    def __str__(self):
        return self.user.username  # String representation of Employee instance, showing username
