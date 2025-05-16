# users/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404

from .forms import SignUpForm, LoginForm, UserForm
from .models import User


class SignUpView(CreateView):

    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")


class LoginView(DjangoLoginView):

    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):

    next_page = reverse_lazy("users:login")


class ProfileDetailView(LoginRequiredMixin, TemplateView):

    template_name = "users/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):

        return self.request.user

    def get_form_kwargs(self):

        return super().get_form_kwargs()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        from django import forms as dj_forms

        if "phone" not in form.fields:
            form.fields["phone"] = dj_forms.CharField(
                required=False,
                label="Phone number",
                widget=dj_forms.TextInput(
                    attrs={
                        "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400",
                        "placeholder": "Phone number",
                    }
                ),
            )

        user = self.request.user
        profile = getattr(user, "seller_profile", None)

        # user‑level
        form.initial.setdefault("phone", user.phone)
        form.initial.setdefault("profile_image", user.profile_image)

        # seller‑level (agency / individual sellers only)
        if profile:
            form.initial.setdefault("logo", profile.logo)
            form.initial.setdefault("bio", profile.bio)
            form.initial.setdefault("company_name", profile.company_name)
            form.initial.setdefault("street", profile.street)
            form.initial.setdefault("city", profile.city)
            form.initial.setdefault("postal_code", profile.postal_code)

        return form

    def form_valid(self, form):

        response = super().form_valid(form)

        user = self.request.user
        cleaned = form.cleaned_data

        if cleaned.get("phone") != user.phone:
            user.phone = cleaned.get("phone", "")
        if cleaned.get("profile_image") is not None:
            user.profile_image = cleaned["profile_image"]
        user.save()

        profile = getattr(user, "seller_profile", None)
        if profile:
            profile.logo = cleaned.get("logo", profile.logo)
            profile.bio = cleaned.get("bio", profile.bio)
            profile.company_name = cleaned.get("company_name", profile.company_name)
            profile.street = cleaned.get("street", profile.street)
            profile.city = cleaned.get("city", profile.city)
            profile.postal_code = cleaned.get("postal_code", profile.postal_code)
            profile.save()

        messages.success(self.request, "Profile updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "users/password_change_done.html"


class PublicProfileView(TemplateView):

    template_name = "users/public_profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seller = get_object_or_404(User, pk=self.kwargs["pk"])
        ctx["seller"] = seller
        if seller.user_type != User.BUYER:
            ctx["profile"] = seller.seller_profile
        ctx["properties"] = seller.properties.filter(is_published=True).order_by(
            "-created_at"
        )
        return ctx
