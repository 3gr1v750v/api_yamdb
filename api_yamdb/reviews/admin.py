from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    )
    list_editable = ('role', 'is_superuser')