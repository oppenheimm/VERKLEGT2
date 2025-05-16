# users/forms.py
import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, SellerProfile

logger = logging.getLogger(__name__)


class SignUpForm(UserCreationForm):
    """Extended sign-up form that collects seller info when needed, now with
    uniform styling for file inputs and textarea."""

    # ───────── basic user fields ─────────
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

    # ───────── seller-specific fields ─────────
    company_name = forms.CharField(required=False, label="Company name (agency)")
    license_number = forms.CharField(required=False, label="License number")
    street = forms.CharField(required=False, label="Street name")
    city = forms.CharField(required=False, label="City")
    postal_code = forms.CharField(required=False, label="Postal code")

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Bio",
    )
    logo = forms.ImageField(required=False, label="Logo (agency)")
    cover_image = forms.ImageField(required=False, label="Cover image")

    # ▶ ONLY User-table fields go here
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

    # ───────── validation & styling tweaks ─────────
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove the “admin” option
        self.fields["user_type"].choices = [
            (k, v) for k, v in User.USER_TYPE_CHOICES if k != User.ADMIN
        ]

        # give file inputs and textarea the same rounded look
        file_style = (
            "w-full text-sm text-gray-900 border border-gray-300 rounded-lg "
            "cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 "
            "focus:ring-indigo-400"
        )
        for fld in ("logo", "cover_image"):
            self.fields[fld].widget.attrs.update({"class": file_style})

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

    # ───────── save extra profile data ─────────
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
            profile.cover_image = self.cleaned_data.get("cover_image")
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


# users/forms.py
# users/forms.py  – put this near the top with the other imports
from .models import User


class ProfileForm(forms.ModelForm):
    # ─── core user fields ─────────────────────────────
    name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    profile_image = forms.ImageField(required=False)

    # ─── seller extras ───────────────────────────────
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
    logo = forms.ImageField(required=False)
    company_name = forms.CharField(required=False)
    license_number = forms.CharField(required=False)
    street = forms.CharField(required=False)
    city = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)

    # inside ProfileForm ─ leave the rest as-is
    logo = forms.ImageField(
        required=False,
        label="Logo",
        widget=forms.ClearableFileInput(
            attrs={
                "id": "id_logo",  # so the <label for="…"> finds it
                "class": "hidden",  # hide the real file element
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["name", "phone", "email", "profile_image", "logo"]

    # Make agency fields mandatory for agency sellers
    def clean(self):
        cleaned = super().clean()
        if self.instance.user_type == User.AGENCY_SELLER:
            for fld in (
                "company_name",
                "license_number",
                "street",
                "city",
                "postal_code",
            ):
                if not cleaned.get(fld):
                    self.add_error(fld, "Required for agency sellers.")
        return cleaned

    # Copy the seller-side data into SellerProfile
    def save(self, commit=True):
        user = super().save(commit=True)

        # store the logo on the SellerProfile that already has a `logo` field
        if user.user_type != User.BUYER:
            sp = user.seller_profile
            if self.cleaned_data.get("logo") is not None:
                sp.logo = self.cleaned_data["logo"]
                sp.save()

        return user
