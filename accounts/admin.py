from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the list view
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    
    # Specify the ordering of the list view
    ordering = ('email',)
    
    # Specify the fields to be used in searching
    search_fields = ('email', 'first_name', 'last_name', 'role')
    
    # Specify the fields to be displayed in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'age', 'gender', 'address', 'mobile_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Specify the fields to be displayed in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    
    # Specify the field to be used as the username field
    username_field = 'email'
    
    # Specify the field to be used as the password field
    password_field = 'password'
