from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SSUser

class SSUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SSUser
        fields = ('email', 'first_name', 'last_name')

class SSUserChangeForm(UserChangeForm):

    class Meta:
        model = SSUser
        fields = UserChangeForm.Meta.fields