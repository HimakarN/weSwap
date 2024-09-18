from django.contrib.auth import authenticate, login, password_validation
from .otp import signup_otp, send_otp, after_signup
from django.core.exceptions import ValidationError
from .decorators import otp_verified_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
import json
import re


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


def user_exists(username='', email=''):
    if username and not email:
        return User.objects.filter(Q(username__iexact=username)).exists()
    elif not username and email:
        return User.objects.filter(Q(email__iexact=email)).exists()
    elif not username and not email:
        raise ValueError("At least one of username or email must be provided")


def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        if action == 'send-otp':
            email = data.get('email')
            if user_exists(email=email):
                return JsonResponse({'success': False, 'message': 'email already in use'})
            else:
                if signup_otp(email, request):
                    return JsonResponse({'success': True, 'message': 'OTP sent successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'enter valid email'})

        elif action == 'verify-otp':
            if data.get('otp') == request.session.get('otp'):
                return JsonResponse({'success': True, 'message': 'OTP verified successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'invalid OTP!'})

        elif action == 'signup':
            # Create a new user
            if user_exists(username=data.get('username')):
                return JsonResponse({'success': False, 'message': 'Username already in use'})
            else:
                user = User.objects.create_user(username=data.get('username'), email=data.get('email'),
                                                 password=data.get('password'))
                recipient_list = [data.get('email')]
                after_signup(user, data.get('gender'), data.get('department'), data.get('current_year'), recipient_list)
                return JsonResponse(
                    {'success': True, 'message': 'Profile created successfully!', 'redirect': reverse('login')})

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
                request.session['otp_verified'] = True
                request.session['reset_email'] = email  # Store email in session
                change_password_url = reverse('change_password')
                return JsonResponse({'success': True, 'message': 'OTP verified!', 'redirect': change_password_url})
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
                return JsonResponse({'error': True, 'message': 'Invalid credentials'})
    else:
        return render(request, 'user_authorization/password_reset.html')


@otp_verified_required
def change_password(request):
    email = request.session.get('reset_email')
    user = User.objects.get(email=email)
    if not email:
        return redirect('password_reset')
    if request.method == 'POST':
        data = json.loads(request.body)
        new_pass = data.get('new_password')
        verify_pass = data.get('verify_password')
        try:
            # Validate the password
            password_validation.validate_password(new_pass, user)
        except ValidationError as e:
            # If the password doesn't meet the validation criteria, return the error messages
            return JsonResponse({'success': False, 'message': ' '.join(e.messages)})

        if new_pass == verify_pass:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_pass)
                user.save()  # Save the user object to persist changes
                return JsonResponse(
                    {'success': True, 'message': 'Password changed successfully', 'redirect': reverse('login')})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Failed to change password'})
    return render(request, 'user_authorization/change_password.html')
