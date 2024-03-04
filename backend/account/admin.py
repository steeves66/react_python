from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ('id', 'email', 'firstname', 'lastname', 'phone_1', 'phone_2', 'is_active', 'is_admin',)
    list_filter = ("is_admin",)
    search_fields = ("username", "email",)
    ordering = ("email", "id")
    fieldsets = (
        ('Personal Info', {
            'fields': ('firstname', 'lastname', 'username', 'phone_1', 'phone_2',)
            }),
        ('User Credentials', {
            'fields': ('email', 'password',)
            }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')
            }),
        )
    add_fieldsets = (
        ('Personal Info', {
            'fields': ('firstname', 'lastname', 'username', 'phone_1', 'phone_2',)
            }),
        ('User Credentials', {
            'fields': ('email', 'password1', 'password2')
            }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')
            }),
        )