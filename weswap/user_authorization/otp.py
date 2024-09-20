import random

from django.conf import settings
from django.core.mail import send_mail

from .models import Profile


def after_signup(user, gender, department, current_year, recipient_list):
    subject = "Welcome to WeSwap! Your Registration is Complete"
    message = f"""Dear {user.username},

Congratulations and welcome to WeSwap!

We’re excited to have you on board. Your registration has been successfully completed, and you are now part of the WeSwap community. Here’s a quick overview of what you can do next:

1. Explore and List Products: Start by browsing the available products or list your own items for borrowing.
2. Manage Your Account: Visit your profile to update your details, set preferences, and manage your listings.
3. Start Swapping: Connect with other users and start exchanging products effortlessly!

Your Account Details:

- Username: {user.username}
- Email: {user.email}

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


def generate_otp():
    return str(random.randint(10000, 99999))


def send_otp(user_otp, email, request):
    otp = generate_otp()
    request.session['otp'] = otp
    subject = 'Your WeSwap OTP for Password Reset'
    message = f"""
    Dear {user_otp.username},

    We received a request to reset your password for your WeSwap account.

    To proceed with resetting your password, please use the following One-Time Password (OTP):

    Your OTP Code: {otp}

    Instructions:
    1. Enter this OTP code on the password reset page of the WeSwap application.
    2. This OTP is valid for 15 minutes.
    3. After verification, you'll be prompted to create a new password.

    Important Security Note:
    If you didn't request a password reset, please ignore this email and ensure your account is secure by checking your recent account activity.

    Need Assistance?
    If you have any questions or need help, don't hesitate to contact our support team at support@weswap.com or visit our Help Center.

    Remember, WeSwap will never ask you to share your password or OTP via email or phone.

    Thank you for using WeSwap. We're committed to keeping your account safe and secure.

    Best regards,
    The WeSwap Security Team
    """
    from_email = settings.EMAIL_HOST_USER
    return send_mail(subject, message, from_email, [email])


def signup_otp(email, request):
    otp = generate_otp()
    request.session['otp'] = otp
    subject = 'Your WeSwap OTP for Email Verification'
    message = f"""
        Dear user,

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
