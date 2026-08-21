from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .forms import SignUpForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def send_html_email(subject, text_content, html_content, to_email):
    """Helper to send email with HTML and text fallback."""
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except Exception as e:
        print("Email sending failed:", e)


def set_user_cookies(response, user):
    """Set cookies securely."""
    cookie_options = {
        'max_age': 7 * 24 * 60 * 60,
        'httponly': True,
        'secure': True,  # Use HTTPS in production
        'samesite': 'Lax'
    }
    response.set_cookie('username', user.username, **cookie_options)
    response.set_cookie('email', user.email, **cookie_options)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Log the user in immediately after signup
            login(request, user)

            # Send welcome email
            send_html_email(
                "Signup Successful - Lost & Found",
                "Your account has been created successfully!",
                "<h1>Welcome to Lost & Found!</h1><p>Your account has been created successfully.</p>",
                user.email,
            )

            response = redirect('home')
            set_user_cookies(response, user)
            return response
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Send login notification email
            send_html_email(
                "Login Notification - Lost & Found",
                f"Hi {user.username}, you have successfully logged in.",
                f"<h1>Hello {user.username}!</h1><p>You have successfully logged in.</p>",
                user.email,
            )

            response = redirect('home')
            set_user_cookies(response, user)
            return response
        else:
            messages.error(request, "Invalid username/email or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    response = redirect('accounts:login')
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def update_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def admin_dashboard(request):
    if request.user.profile.user_type != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('accounts:profile')
    return render(request, 'accounts/admin_dashboard.html')
