# users/views.py

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, 
    PasswordChangeDoneView
    , LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.views.generic.edit import UpdateView

from .forms import SignUpForm, LoginForm, ProfileForm
from .models import User

class SignUpView(CreateView):
    """
    Renders a signup form and handles user registration.
    Uses Django's built-in CreateView under the hood.
    """
    form_class    = SignUpForm 
    template_name = 'users/signup.html'
    success_url   = reverse_lazy('users:login')

class LoginView(DjangoLoginView):
    """
    Renders a login form and handles authentication.
    Uses Django's built-in LoginView under the hood.
    """
    form_class    = LoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
class LogoutView(DjangoLogoutView):
    """
    Handles user logout.
    Uses Django's built-in LogoutView under the hood.
    """
    template_name = 'users/logout.html'
    next_page = reverse_lazy('users:login')


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    """Show profile info with Edit / Change Password buttons."""
    template_name = 'users/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit name, email, profile image only."""
    form_class    = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url   = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Separate page for changing password."""
    template_name = 'users/password_change.html'
    success_url   = reverse_lazy('users:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'