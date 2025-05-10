# users/urls.py

from django.urls import path
from .views import SignUpView, LoginView, LogoutView, ProfileDetailView, ProfileEditView, CustomPasswordChangeView, CustomPasswordChangeDoneView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/',  LoginView.as_view(),    name='login'),
    path('logout/', LogoutView.as_view(),   name='logout'),
    path('profile/',           ProfileDetailView.as_view(),           name='profile'),
    path('profile/edit/',      ProfileEditView.as_view(),             name='profile_edit'),
    path('password_change/',   CustomPasswordChangeView.as_view(),    name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]
