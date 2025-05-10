# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Enter your username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'you@example.com',
        })
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Enter a secure password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Repeat your password',
        })
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
        }),
        label='Select User Type',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Password',
        })
    )