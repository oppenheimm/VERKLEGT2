# users/views.py

from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm, LoginForm

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