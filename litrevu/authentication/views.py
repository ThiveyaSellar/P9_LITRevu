from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from . import forms


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Authentifier l'utilisateur avec authenticate et login
            # authenticate retourne l'utilisateur correspondant sinon None
            user = authenticate(
                username=form.cleaned_data['username'].lower(),
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            message = "Identifiants invalides."
    context = {
        'form': form,
        'message': message,
    }
    return render(request, "authentication/login.html", context=context)


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            user.save()
            login(request, user)
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'authentication/signup.html', context=context)
