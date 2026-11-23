from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class VerifyForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP',
            'class': 'form-control',
            'autocomplete': 'one-time-code',
        })
    )

class EditProfileForm(forms.ModelForm):
    class Meta :
        model = CustomUser
        fields = ['first_name', 'last_name', 'about', 'profile_image']

