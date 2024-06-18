# company_management_system

## Introduction

The Company Management System is a web application designed to streamline and manage various aspects of a company's operations. This system provides functionalities for user authentication, role-based access control, department management, task assignment, and employee management. The application is built using Django and deployed using Docker on Render.

### Live Demo

You can access a live demo of the application [here](https://skynet-5c65.onrender.com/).


## Table of Contents

1. [Features](#Features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Functionality](#functionality)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- **User Authentication**: Secure signup and login functionalities.
- **Role Management**: Assign roles (employee, manager) to users.
- **Department Management**: Create, edit, delete, and list departments.
- **Task Management**: Create, assign, edit, delete, and list tasks.
- **Employee Management**: Manage employees within departments.
- **Role-based Access Control**: Managers have additional permissions to manage departments and employees.

## Installation

### Prerequisites

- Python 3.8+
- Django

### Setup Instructions

1. **Clone the repository:**

```bash
   git clone https://github.com/souuja-ops/company_management_system.git
   cd company_management_system
```

2. **Create a virtual environment:**

```bash
   python -m venv env
```

3. **Activate the virtual environment:**

   - **Windows:**

     ```bash
     .\env\Scripts\activate
     ```

   - **Linux/macOS:**

     ```bash
      source env/bin/activate
     ```

4. **Install dependencies:**

   ```bash
    pip install -r requirements.txt
   ```

5. **Apply migrations:**

   ```bash
    python manage.py migrate
   ```

6. **Create a superuser (optional):**

   ```bash
    python manage.py createsuperuser
   ```
7. **Fetch tasks from JSON Placeholder API (optional):**

   Populate the database with sample data using the JSON Placeholder API:

   ```bash
   python manage.py fetch_tasks
   ```

## Usage

1. **Run the development server:**

   ```bash
    python manage.py runserver
   ```

2. **Access the application:**

   Open a web browser and go to `http://localhost:8000`

3. **Login as an admin:**

   - Use the superuser credentials created earlier to access the admin panel.

## Project Structure

Explain the structure of your project files and directories.

## Project Structure

```plaintext
company_management/
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── fetch_tasks.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── core/
│           ├── landing_page.html
│           ├── signup.html
│           ├── login.html
│           ├── manager_dashboard.html
│           ├── employee_dashboard.html
│           ├── department_list.html
│           ├── department_form.html
│           ├── department_detail.html
│           ├── department_confirm_delete.html
│           ├── employee_list.html
│           ├── move_employee.html
│           ├── delete_employee.html
│           ├── task_list.html
│           ├── task_form.html
│           ├── task_confirm_delete.html
│           └── assign_task.html
├── company_management/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Functionality

#### Authentication

- **Signup**: New users can create an account with a default role of 'employee'.
- **Login**: Existing users can log in with their credentials and select their role.
- **Role-Based Access Control**: Different functionalities and pages are accessible based on the user's role.

#### Department Management (Managers Only)

- **Create Department**: Managers can create new departments.
- **Edit Department**: Managers can edit existing departments.
- **Delete Department**: Managers can delete departments.
- **View Department Details**: Managers can view details of a department, including the list of employees in the department.

#### Task Management

- **Create Task**: Managers can create tasks and assign them to employees.
- **Edit Task**: Managers can edit task details.
- **Delete Task**: Managers can delete tasks.
- **Assign Task**: Managers can assign tasks to employees.
- **View Task List**: Both managers and employees can view the list of tasks. Employees see only their assigned tasks.

#### Employee Management (Managers Only)

- **Move Employee**: Managers can move employees between departments.
- **Delete Employee**: Managers can delete employees from the system.

#### Dashboard

- **Manager Dashboard**: Provides an overview of tasks, departments, and employees, including statistics on task completion rates.
- **Employee Dashboard**: Lists tasks assigned to the logged-in employee, allowing them to mark tasks as done or in progress.

**Employee Capabilities:**
- Access to the employee dashboard with their task list.
- Mark tasks as completed or in progress.
- View assigned tasks.

### Example Usage

1. **Login as System Administrator**:
   - Go to [Admin Interface](https://skynet-5c65.onrender.com/admin).
   - Use the credentials `Username: coder`, `Password: 1234`.

2. **Login as Manager**:
   - Go to [Login](https://skynet-5c65.onrender.com/login).
   - Use the credentials `Username: manager`, `Password: 1234`.
   - Select 'manager' in the role section.

3. **Login as Employee**:
   - Go to [Login](https://skynet-5c65.onrender.com/login).
   - Use the credentials `Username: employee`, `Password: 1234`.
   - Select 'employee' in the role section.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add feature'`)
5. Push to the branch (`git push origin feature`)
6. Create a new Pull Request


## License

This project is licensed under the MIT License. See the full text of the license below:

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

By using this software, you agree to the terms and conditions outlined in this license.

---

