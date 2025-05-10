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

    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400',
            'placeholder': 'Your phone number',
        }),
        label="Phone number"
    )
    
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400',
            'placeholder': 'Company name (if agency)',
        }),
        label="Company name (agency sellers only)"
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type', 'phone', 'company_name', 'password1', 'password2')

    def clean(self):
        cleaned = super().clean()
        user_type = cleaned.get('user_type')
        company = cleaned.get('company_name')
        if user_type == User.AGENCY_SELLER and not company:
            self.add_error('company_name', 'Company name is required for agency sellers.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit)
        # Save phone & company onto the right profile
        if user.user_type == User.BUYER:
            user.buyer_profile.phone = self.cleaned_data['phone']
            user.buyer_profile.save()
        else:
            user.seller_profile.phone        = self.cleaned_data['phone']
            user.seller_profile.company_name = self.cleaned_data['company_name']
            user.seller_profile.save()
        return user

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
    
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': (
                'w-full px-4 py-2 '
                'border border-gray-300 '
                'rounded-lg focus:outline-none '
                'focus:ring-2 focus:ring-indigo-400'
            ),
            'placeholder': 'Phone Number',
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
        fields = ['name', 'phone', 'email', 'profile_image']