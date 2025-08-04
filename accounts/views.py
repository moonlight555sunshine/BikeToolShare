from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from .forms import RegisterForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'Register',
            'subtitle': 'Register for a User account',
        })
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'form_page.html', {
                'form': form,
                'title': 'Register',
                'subtitle': 'Register for a User account',
            })

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'Login',
            'subtitle': 'Log in to your account',
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
        })

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')