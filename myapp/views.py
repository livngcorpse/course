from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def books(request):
    return render(request, 'books.html')

def settings(request):
    return render(request, 'settings.html')

def about(request):
    return render(request, 'about.html')

def feedback(request):
    return render(request, 'feedback.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'signup.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def add_syllabus(request):
    if request.user.role != "Faculty":
        return redirect('home')
    return render(request, 'add_syllabus.html')

@login_required
def requests(request):
    if request.user.role != "Admin":
        return redirect('home')
    return render(request, 'requests.html')

@login_required
def upload(request):
    if request.user.role != "Admin":
        return redirect('home')
    return render(request, 'upload.html')

def logout_view(request):
    logout(request)
    return redirect('login')