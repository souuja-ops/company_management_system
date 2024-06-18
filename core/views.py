from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Role, Department, Employee, Task
from .forms import CustomSignupForm, DepartmentForm, TaskForm, MoveEmployeeForm, CustomAuthenticationForm
from django.db.models import Count

# Landing page view
def landing_page(request):
    return render(request, 'core/landing_page.html')

# User signup view
def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after signup
            return redirect('employee_dashboard')
    else:
        form = CustomSignupForm()
    
    return render(request, 'core/signup.html', {'form': form})

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in the user
            # Redirect based on user role
            try:
                role = user.role
                if role.role == 'manager':
                    return redirect('manager_dashboard')
                else:
                    return redirect('employee_dashboard')
            except Role.DoesNotExist:
                form.add_error(None, "No role assigned to this user. Contact the system administrator.")
        return render(request, 'core/login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

# Redirect to appropriate dashboard based on user role
@login_required
def dashboard_redirect(request):
    if hasattr(request.user, 'role') and request.user.role.role == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('employee_dashboard')

# Manager dashboard view
@login_required
def manager_dashboard(request):
    if not (hasattr(request.user, 'role') and request.user.role.role == 'manager'):
        messages.error(request, 'Permission denied. Only managers can access the manager dashboard.')
        return redirect('employee_dashboard')

    departments = Department.objects.all()
    tasks = Task.objects.all()
    employees = Employee.objects.all()
    
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    task_completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    context = {
        'departments': departments,
        'tasks': tasks,
        'employees': employees,
        'task_completion_rate': task_completion_rate,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'core/manager_dashboard.html', context)

# List all departments view
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments})

# Create department view
@login_required
def department_create(request):
    if not (hasattr(request.user, 'role') and request.user.role.role == 'manager'):
        messages.error(request, 'Permission denied. Only managers can create departments.')
        return redirect('department_list')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'core/department_form.html', {'form': form})

# View department details
@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    employees = Employee.objects.filter(department=department)
    return render(request, 'core/department_detail.html', {'department': department, 'employees': employees})

# Edit department view
@login_required
def department_edit(request, pk):
    if not (hasattr(request.user, 'role') and request.user.role.role == 'manager'):
        messages.error(request, 'Permission denied. Only managers can edit departments.')
        return redirect('department_list')

    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'core/department_form.html', {'form': form})

# Delete department view
@login_required
def department_delete(request, pk):
    if not (hasattr(request.user, 'role') and request.user.role.role == 'manager'):
        messages.error(request, 'Permission denied. Only managers can delete departments.')
        return redirect('department_list')

    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('department_list')
    
    return render(request, 'core/department_confirm_delete.html', {'department': department})

# Move employee view
@login_required
def move_employee(request, pk):
    if not (hasattr(request.user, 'role') and request.user.role.role == 'manager'):
        messages.error(request, 'Permission denied. Only managers can move employees.')
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)
    departments = Department.objects.all()

    if request.method == 'POST':
        form = MoveEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.user.username} moved successfully.')
            return redirect('employee_list')
    else:
        form = MoveEmployeeForm(instance=employee)

    return render(request, 'core/move_employee.html', {'form': form, 'employee': employee, 'departments': departments})

# Delete employee view
@login_required
def delete_employee(request, pk):
    if not (hasattr(request.user, 'role') and request.user.role.role == 'manager'):
        messages.error(request, 'Permission denied. Only managers can delete employees.')
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, f'Employee {employee.user.username} removed from the organization.')
        return redirect('employee_list')

    return render(request, 'core/delete_employee.html', {'employee': employee})

# List all employees view
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'core/employee_list.html', {'employees': employees})

# List all tasks view
@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'core/task_list.html', {'tasks': tasks})

# Create task view
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'core/task_form.html', {'form': form})

# Edit task view
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'core/task_form.html', {'form': form, 'task': task})

# Delete task view
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return render(request, 'core/task_confirm_delete.html', {'task': task})

# Assign task view
@login_required
def assign_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        assigned_to_id = request.POST.get('employee')  # Get selected employee ID from POST data
        assigned_to = get_object_or_404(User, pk=assigned_to_id)
        task.assigned_to = assigned_to
        task.save()
        messages.success(request, f'Task "{task.title}" assigned to {assigned_to.username}.')
        return redirect('task_list')
    
    employees = User.objects.filter(role__role='employee')  # Fetch all users with role 'employee'
    return render(request, 'core/assign_task.html', {'task': task, 'employees': employees})

# Employee dashboard view
@login_required
def employee_dashboard(request):
    # Filter out tasks that are completed
    tasks = Task.objects.filter(assigned_to=request.user, completed=False)

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')

        task = get_object_or_404(Task, pk=task_id)
        if task.assigned_to != request.user:
            messages.error(request, 'You are not authorized to modify this task.')
            return redirect('employee_dashboard')

        if action == 'mark_done':
            task.completed = True
            task.save()
            messages.success(request, f'Task "{task.title}" marked as done.')
        elif action == 'mark_in_progress':
            task.completed = False
            task.save()
            messages.info(request, f'Task "{task.title}" marked as in progress.')
        elif action == 'clear_completed':
            task.delete()
            messages.success(request, f'Task "{task.title}" cleared from task board.')

        return redirect('employee_dashboard')

    context = {
        'tasks': tasks,
    }
    return render(request, 'core/employee_dashboard.html', context)