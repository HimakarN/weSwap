# Create your views here.
import json
import random
import re

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile


def home(request):
    return render(request, 'user_authorization/home.html')


def login_view(request):
    global user
    user = None
    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True
        user_email = request.POST['user|email']
        password = request.POST['password']
        if re.match(r"[^@]+@[^@]+\.[^@]+", user_email) is not None:
            print('email entered')
            try:
                user = User.objects.get(email=user_email)
                user = authenticate(request, username=user.username, password=password)
            except:
                messages.error(request, 'Invalid credentials')
                return render(request, 'user_authorization/login.html', {'error': True})
        else:
            user = authenticate(request, username=user_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'user_authorization/login.html', {'error': True})
    return render(request, 'user_authorization/login.html')


def after_signup(user, gender, department, current_year, recipient_list):
    subject = "Welcome to WeSwap! Your Registration is Complete"
    message = f"""Dear {user.username},

Congratulations and welcome to WeSwap!

We’re excited to have you on board. Your registration has been successfully completed, and you are now part of the WeSwap community. Here’s a quick overview of what you can do next:

1. **Explore and List Products:** Start by browsing the available products or list your own items for borrowing.
2. **Manage Your Account:** Visit your profile to update your details, set preferences, and manage your listings.
3. **Start Swapping:** Connect with other users and start exchanging products effortlessly!

Your Account Details:

- **Username:** {user.username}
- **Email:** {user.email}

Need Help? If you have any questions or need assistance, feel free to reach out to our support team at support@weswap.com or visit our Help Center.

Thank you for choosing WeSwap. We hope you have a great experience and enjoy all the benefits of our platform.

Best regards,
The WeSwap Team
"""
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, recipient_list)
    Profile.objects.create(
        user=user,
        gender=gender,
        department=department,
        current_year=current_year)


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        department = request.POST['department']
        current_year = request.POST['current_year']

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        recipient_list = [email]
        after_signup(user, gender, department, current_year, recipient_list)

        return render(request, 'user_authorization/signup_success.html')

    return render(request, 'user_authorization/signup.html')


def password_reset(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        email = data.get('email')

        if action == 'send_otp':
            user_reset = User.objects.filter(email=email).first()
            if user_reset:
                res = send_otp(user_reset, email, request)
                if res:
                    return JsonResponse({'success': True, 'message': 'OTP sent successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Unable to send OTP.'})
            else:
                messages.error(request, 'Invalid credentials')
                return JsonResponse({'error': True, 'message': 'enter valid email!'})

        elif action == 'verify_otp':
            otp = data.get('otp')
            user_otp = request.session.get('otp')
            if otp == user_otp:
                return JsonResponse({'success': True, 'message': 'OTP verified!'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP.'})

        elif action == 'resend_otp':
            user_reset = User.objects.filter(email=email).first()
            if user_reset:
                res = send_otp(user_reset, email, request)
                if res:
                    return JsonResponse({'success': True, 'message': 'OTP resent successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Unable to send OTP.'})
            else:
                return render(request, 'user_authorization/password_reset.html', {'error': True})
    else:
        return render(request, 'user_authorization/password_reset.html')


def generate_otp():
    return str(random.randint(10000, 99999))


def send_otp(user_otp, email, request):
    otp = generate_otp()
    request.session['otp'] = otp
    subject = 'Your WeSwap OTP for Email Verification'
    message = f"""
        Dear {user_otp.username},

        Thank you for registering with WeSwap!

        To complete your registration and verify your email address, please use the following One-Time Password (OTP):

        Your OTP Code: {otp}

        Instructions:
        Enter the OTP code on the verification page of the WeSwap application.
        The OTP is valid for 15 minutes. If you did not request this OTP, please disregard this email.

        Need Assistance?
        If you have any questions or need help, feel free to contact our support team at support@weswap.com or visit our Help Center.

        Thank you for joining WeSwap. We’re excited to have you as part of our community!

        Best regards,
        The WeSwap Team
        """
    from_email = settings.EMAIL_HOST_USER
    return send_mail(subject, message, from_email, [email])

