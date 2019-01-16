from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import SSUserCreationForm, SSUserChangeForm
from .models import SSUser

class SSUserAdmin(UserAdmin):
    add_form = SSUserCreationForm
    form = SSUserChangeForm
    model = SSUser
    list_display = ['email', 'first_name', 'last_name']
    ordering = ['email']

admin.site.register(SSUser, SSUserAdmin)
