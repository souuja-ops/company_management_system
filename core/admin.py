
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Role

# Custom admin for Role model
class RoleAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('user', 'role')
    
    # Actions available in the admin list view
    actions = ['make_manager', 'make_employee']

    # Action method to change selected roles to manager
    def make_manager(self, request, queryset):
        # Update the queryset to set role='manager' for selected objects
        updated = queryset.update(role='manager')
        # Notify the user with a success message
        self.message_user(request, f"{updated} role(s) changed to manager.")
    make_manager.short_description = "Change selected roles to manager"  # Action description

    # Action method to change selected roles to employee
    def make_employee(self, request, queryset):
        # Update the queryset to set role='employee' for selected objects
        updated = queryset.update(role='employee')
        # Notify the user with a success message
        self.message_user(request, f"{updated} role(s) changed to employee.")
    make_employee.short_description = "Change selected roles to employee"  # Action description

# Register the Role model with its custom admin
admin.site.register(Role, RoleAdmin)

# Inline admin for Role model within the User admin
class RoleInline(admin.StackedInline):
    model = Role
    can_delete = False

# Extend the BaseUserAdmin to include the RoleInline
class UserAdmin(BaseUserAdmin):
    inlines = (RoleInline,)  # Add RoleInline to the User admin

# Unregister the default User admin and register the extended User admin with RoleInline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
