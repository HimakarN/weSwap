from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'user_authorization/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'user_authorization/login_success.html')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'user_authorization/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        department = request.POST['department']
        current_year = request.POST['current_year']

        # Create a new user
        User.objects.create_user(username=username, email=email, password=password)

        return render(request, 'user_authorization/signup_success.html')

    return render(request, 'user_authorization/signup.html')
