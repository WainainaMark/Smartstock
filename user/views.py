import random
import json
from django.shortcuts import render, redirect
from .forms import UserForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def signIn(request):
    # if request.user.is_authenticated:
    #     return redirect('/home')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            user.save()
            # messages.success(request, "Account created successfully! Kindly login on the next window")
            return redirect('/login')
    else:
        form = UserForm()
    return render(request, 'user/signin.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Invalid username or password')
    response = render(request, 'user/login.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response

def terms(request):
    return render(request, 'user/TermsCondition.html')

def privacy(request):
    return render(request, 'user/privacyPolicy.html')

otp_storage = {}

def generate_otp():
    """Generate a 6-digit OTP"""    
    return str(random.randint(100000, 999999))

def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            
            # Store email and OTP in session
            request.session['reset_email'] = email
            request.session['otp'] = otp
            request.session.set_expiry(300)  # OTP expires in 5 minutes

            # Send OTP via email
            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email.")
            return redirect('verifyOTP')

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return render(request, 'user/forgotPassword.html')

def verifyOTP(request):
    """Handle OTP verification"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Get data from AJAX request
            email = request.session.get('reset_email')
            stored_otp = request.session.get('otp')
            user_otp = data.get('otp')

            if not email or not stored_otp:
                return JsonResponse({"success": False, "message": "Session expired. Request a new OTP."})

            if stored_otp == user_otp:
                del request.session['otp']  # Remove OTP after successful verification
                return JsonResponse({"success": True, "redirect_url": "/reset_password"})  # Redirect user

            return JsonResponse({"success": False, "message": "Invalid OTP. Try again."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid request format."})

    return JsonResponse({"success": False, "message": "Invalid request."})

def reset(request):
    return render(request, 'user/resetPassword.html')