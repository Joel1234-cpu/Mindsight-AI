from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
