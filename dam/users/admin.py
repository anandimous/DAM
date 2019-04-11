from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from dam.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name', 'email')
