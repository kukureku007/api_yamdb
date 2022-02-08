from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
        'date_joined'
    )
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'
    list_editable = ('role','is_staff')
    pass
