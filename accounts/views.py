from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from .forms import RegisterForm, UserInfoForm
from .models import UserProfile


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'Register',
            'subtitle': 'Register for a User account',
            'button_text': 'Register',
        })
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created. Please fill out user info below.')
            return redirect('update_info')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'form_page.html', {
                'form': form,
                'title': 'Register',
                'subtitle': 'Register for a User account',
                'button_text': 'Register',
            })

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'Login',
            'subtitle': 'Log in to your account',
            'button_text': 'Login',
        })
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            messages.success(request, 'You are now logged in as %s' % user.username)
            return redirect(next_url)
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'Login',
            'subtitle': 'Log in to your account',
            'button_text': 'Login',
        })

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')

class UpdateInfoView(View):
    def get(self, request):
        current_user = UserProfile.objects.get(user_id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'Update Info',
            'subtitle': 'Update your info',
            'button_text': 'Update',
            'profile_picture': current_user.profile_picture.url if current_user.profile_picture else None
        })
    def post(self, request):
        if request.user.is_authenticated:
            current_user = UserProfile.objects.get(user_id=request.user.id)
            form = UserInfoForm(request.POST or None, request.FILES, instance=current_user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your info has been updated')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'form_page.html', {
                    'form': form,
                    'title': 'Update Info',
                    'subtitle': 'Update your info',
                    'button_text': 'Update',
                    'profile_picture': current_user.profile_picture.url if current_user.profile_picture else None
                })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')

class AccountView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user_profile = UserProfile.objects.get(user_id=request.user.id)
            return render(request, "account.html", {
                'title': 'Your account',
                'subtitle': '',
                'current_user_profile': current_user_profile,
            })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')