
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Role, Department, Task, Employee

# Form for user signup
class CustomSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Assign default role as Employee when committing the user creation
            user_role = Role(user=user, role='employee')
            user_role.save()
        return user

# Custom authentication form with role selection
class CustomAuthenticationForm(AuthenticationForm):
    role = forms.ChoiceField(choices=[('employee', 'Employee'), ('manager', 'Manager')])

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        role = cleaned_data.get('role')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                try:
                    user_role = self.user_cache.role
                    # Check if user has the appropriate role for login
                    if role == 'manager' and user_role.role != 'manager':
                        raise forms.ValidationError("You are not authorized to login as a manager.")
                    elif role == 'employee' and user_role.role != 'employee':
                        raise forms.ValidationError("You are not authorized to login as an employee.")
                except Role.DoesNotExist:
                    raise forms.ValidationError("No role assigned to this user. Contact the system administrator.")
        
        return cleaned_data

# Form for creating/updating a department
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

# Form for creating/updating a task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'completed']

# Form for moving an employee to another department
class MoveEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['department']

# Utility function to set a user's role
def set_user_role(user, new_role):
    try:
        role, created = Role.objects.get_or_create(user=user)
        role.role = new_role
        role.save()
    except Role.MultipleObjectsReturned:
        raise ValidationError("Multiple roles found for this user.")
