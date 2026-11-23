from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class VerifyForm(forms.Form):
    otp = forms.CharField(max_length=6)

class EditProfileForm(forms.ModelForm):
    class Meta :
        model = CustomUser
        fields = ['first_name', 'last_name', 'about', 'profile_image']

