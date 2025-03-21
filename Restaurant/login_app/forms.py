from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    ACCESS_LEVEL_CHOICES = [
        ("kelner", "Kelner Access"),
        ("manager", "Manager Access"),
    ]
    access_level = forms.ChoiceField(
        choices=ACCESS_LEVEL_CHOICES, widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "access_level")
        widgets = {
            "username": forms.TextInput(attrs={"required": True}),
            "password1": forms.PasswordInput(attrs={"required": True}),
            "password2": forms.PasswordInput(attrs={"required": True}),
            "access_level": forms.RadioSelect(attrs={"required": True}),
        }
