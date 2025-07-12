from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'location', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
