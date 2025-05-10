# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Select User Type",
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'user_type',    # ← include here
            'password1',
            'password2',
        )