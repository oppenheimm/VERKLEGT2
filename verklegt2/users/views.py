# users/views.py

from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class    = SignUpForm 
    template_name = 'users/signup.html'
    success_url   = reverse_lazy('users:login')

class LoginView(DjangoLoginView):
    """
    Renders a login form and handles authentication.
    Uses Django's built-in LoginView under the hood.
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # optional: send already-logged-in users elsewhere

class LogoutView(DjangoLogoutView):
    """
    Logs the user out and redirects to login page.
    """
    next_page = reverse_lazy('users:login')