from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class PrivateCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model =User
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_private=True
        if commit:
            user.save()
        return user

class PublicCreateFrom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=User
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_public=True
        if commit:
            user.save()
        return user