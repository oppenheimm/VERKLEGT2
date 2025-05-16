from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, SellerProfile


class SignUpForm(UserCreationForm):
    """Extended sign-up form that collects seller info when needed, now with
    uniform styling for file inputs and textarea."""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Enter your username",
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Full Name",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "you@example.com",
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Enter a secure password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Repeat your password",
            }
        ),
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label="Select User Type",
        widget=forms.Select(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
            }
        ),
    )
    phone = forms.CharField(
        required=False,
        label="Phone number",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Your phone number",
            }
        ),
    )

    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Company name (if agency)",
            }
        ),
        label="Company name (agency sellers only)",
    )
    license_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "License number (if agency)",
            }
        ),
        label="License number (agency sellers only)",
    )
    street = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Street address (if agency)",
            }
        ),
        label="Street address (agency sellers only)",
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "City (if agency)",
            }
        ),
        label="City (agency sellers only)",
    )
    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Postal code (if agency)",
            }
        ),
        label="Postal code (agency sellers only)",
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Bio",
    )
    logo = forms.ImageField(required=False, label="Logo (agency)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "name",
            "email",
            "user_type",
            "phone",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user_type"].choices = [
            (k, v) for k, v in User.USER_TYPE_CHOICES if k != User.ADMIN
        ]

        file_style = (
            "w-full text-sm text-gray-900 border border-gray-300 rounded-lg "
            "cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 "
            "focus:ring-indigo-400"
        )

        self.fields["bio"].widget.attrs.update(
            {
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                "focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Tell buyers about yourself",
            }
        )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("user_type") == User.AGENCY_SELLER:
            required = (
                "company_name",
                "license_number",
                "street",
                "city",
                "postal_code",
            )
            for fld in required:
                if not cleaned.get(fld):
                    self.add_error(fld, "Required for agency sellers.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=True)

        if user.user_type != User.BUYER:
            profile = user.seller_profile
            profile.company_name = self.cleaned_data.get("company_name", "")
            profile.license_number = self.cleaned_data.get("license_number", "")
            profile.street = self.cleaned_data.get("street", "")
            profile.city = self.cleaned_data.get("city", "")
            profile.postal_code = self.cleaned_data.get("postal_code", "")
            profile.logo = self.cleaned_data.get("logo")
            profile.bio = self.cleaned_data.get("bio", "")
            profile.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full px-4 py-2 "
                    "border border-gray-300 "
                    "rounded-lg focus:outline-none "
                    "focus:ring-2 focus:ring-indigo-400"
                ),
                "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": (
                    "w-full px-4 py-2 "
                    "border border-gray-300 "
                    "rounded-lg focus:outline-none "
                    "focus:ring-2 focus:ring-indigo-400"
                ),
                "placeholder": "Password",
            }
        )
    )


class UserForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:ring-2 focus:ring-indigo-400",
            }
        ),
    )
    logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:ring-2 focus:ring-indigo-400",
            }
        ),
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Tell your story.",
            }
        ),
    )
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Company name",
            }
        ),
    )
    street = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Street address",
            }
        ),
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400",
                "placeholder": "City",
            }
        ),
    )
    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400",
                "placeholder": "Postal code",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                    "focus:ring-2 focus:ring-indigo-400",
                    "placeholder": "First name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                    "focus:ring-2 focus:ring-indigo-400",
                    "placeholder": "Email",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.profile_instance = kwargs.pop("profile_instance", None)
        super().__init__(*args, **kwargs)

        if self.profile_instance:
            self.fields["profile_image"].initial = self.profile_instance.profile_image
            self.fields["logo"].initial = self.profile_instance.logo
            self.fields["company_name"].initial = self.profile_instance.company_name
            self.fields["company_address"].initial = (
                self.profile_instance.company_address
            )
            self.fields["registration_number"].initial = (
                self.profile_instance.registration_number
            )

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = self.profile_instance

        if profile:
            profile.profile_image = self.cleaned_data.get(
                "profile_image", profile.profile_image
            )
            profile.logo = self.cleaned_data.get("logo", profile.logo)
            profile.company_name = self.cleaned_data.get("company_name")
            profile.street = self.cleaned_data.get("company_address")
            profile.city = self.cleaned_data.get("city")
            profile.postal_code = self.cleaned_data.get("postal_code")
            profile.bio = self.cleaned_data.get("bio", profile.bio)  # ← added line
            profile.save()

        return user
