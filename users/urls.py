from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    path('password-change-done/', PasswordChangeDone.as_view(), name='password_change_done'),
]