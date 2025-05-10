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


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Full Name',
        })
    )
    email = forms.EmailField(
        required=True,
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
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': (
                'block w-full text-sm text-gray-500 '
                'file:border file:border-gray-300 '
                'file:rounded-lg file:py-2 file:px-4 '
                'file:text-gray-700 focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            )
        })
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'profile_image']