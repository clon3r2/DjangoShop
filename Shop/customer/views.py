from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from core.models import User
from django.contrib import messages
from .models import Customer
from django.contrib.auth import views as auth_views


# Create your views here.


class UserRegisterView(View):
    """
        View for User Registration
    """
    template_name = 'customer/register.html'
    form = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        """
            checks if user is already logged in or not
        """
        if request.user.is_authenticated:  # a user is already logged in
            return redirect('product:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
            sends register template to customer
        """
        form = UserRegistrationForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
            gets Registration form data and validates
        """
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = User.objects.create_user(phone=cd['phone'], email=cd['email'], password=cd['password1'])
            Customer.objects.create(user=new_user, gender=cd['gender'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('product:home')
        else:  # user sends wrong data in register form
            return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    """
        View for User login
    """
    template_name = 'customer/login.html'
    form = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        """
            checks if user is already logged in or not
        """
        if request.user.is_authenticated:
            return redirect('product:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
            sends login template to customer
        """
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        """
            gets Login form data and validates
        """
        form = self.form(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request, username=clean_data['phone'], password=clean_data['password1'])
            if user is not None:  # user exists and passed of authentication
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('product:home')
            else:
                messages.error(request, 'username or password is not correct', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    """
        View for User Logout
    """
    def get(self, request):
        logout(request)
        messages.success(request, "you've been logged out successfully", 'success')
        return redirect('product:home')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'customer/password_reset_form.html'
    success_url = reverse_lazy('customer:password_reset_done')
    email_template_name = 'customer/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'customer/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'customer/password_reset_confirm.html'
    success_url = reverse_lazy('customer:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'customer/password_reset_complete.html'