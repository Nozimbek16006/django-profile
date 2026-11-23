from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .forms import RegisterForm, VerifyForm, EditProfileForm
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .service import UserService
from django.contrib.auth.mixins import LoginRequiredMixin



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('verify')

    def form_valid(self, form):
        UserService.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)

class VerifyView(FormView):
    form_class = VerifyForm
    template_name = 'users/verify.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        otp = form.cleaned_data['otp']

        success = UserService.verify_user(otp)

        if not success:
            form.add_error('otp', 'OTP is invalid or expired!')
            return self.form_invalid(form)

        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('password_change_done')
    
    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully")
        return super().form_valid(form)

class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "users/password_change_done.html"