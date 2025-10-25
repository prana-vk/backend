from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from .models import LoginAttempt
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
import random
from datetime import timedelta
from .models import PasswordResetOTP
from .models import SignupOTP


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Use email as username for simplicity
        username = email

        # New behavior: explicitly check for existing user and return an error
        # if the email is already registered.
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=username).exists():
            return Response({'error': 'Sorry, user already exists'}, status=status.HTTP_409_CONFLICT)

        # Create the user and return token
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Signup successful', 'token': token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        # Explicitly check whether the user exists and return a clear error
        # if not found. This changes behavior from a generic "invalid"
        # response to a direct "user does not exist" message as requested.
        if not User.objects.filter(email__iexact=email).exists():
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check or create LoginAttempt tracker
        attempt, _ = LoginAttempt.objects.get_or_create(email=email)
        if attempt.is_locked():
            locked_until = attempt.locked_until
            return Response({'error': 'Account locked due to multiple failed attempts', 'locked_until': locked_until}, status=status.HTTP_403_FORBIDDEN)

        # Authenticate using email as username
        user = authenticate(username=email, password=password)
        if not user:
            # record failure
            attempt.record_failure()
            remaining = max(0, 5 - attempt.failed_attempts)
            return Response({'error': 'Invalid credentials', 'remaining_attempts': remaining}, status=status.HTTP_401_UNAUTHORIZED)

        # Successful login: reset attempts
        attempt.reset()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful', 'token': token.key})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # New behavior: explicitly inform caller that email is not registered
            return Response({'error': 'This email is not found in database'}, status=status.HTTP_404_NOT_FOUND)

        # generate token & uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # build reset link pointing to frontend
        frontend_base = getattr(settings, 'FRONTEND_URL', 'https://gi-yatra-frontend.vercel.app')
        reset_link = f"{frontend_base.rstrip('/')}/reset-password/?uid={uid}&token={token}"

        # send email (best-effort)
        subject = 'Reset your GI Yatra password'
        message = f"Click the link to reset your password: {reset_link}\nIf you did not request this, ignore this email."
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
        try:
            send_mail(subject, message, from_email, [email], fail_silently=False)
        except Exception:
            # do not fail hard if email sending is not configured
            pass

        return Response({'message': 'If this email exists, a password reset link has been sent.'})


def password_reset_page(request):
    """Template view: ask for email, send OTP and redirect to confirm page."""
    ctx = {}
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            ctx['error'] = 'Please enter your email.'
            return render(request, 'accounts/password_reset_request.html', ctx)

        # Generate OTP and create record only if user exists; don't reveal existence
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            code = f"{random.randint(100000, 999999):06d}"
            now = timezone.now()
            otp = PasswordResetOTP.objects.create(
                email=email,
                otp_code=code,
                expires_at=now + timedelta(minutes=5),
            )

            # send otp by email (best-effort)
            subject = 'Your GI Yatra password reset code'
            message = f"Your password reset code is: {code}\nThis code is valid for 5 minutes.\nIf you did not request this, ignore this email."
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', None))
            try:
                send_mail(subject, message, from_email, [email], fail_silently=False)
            except Exception:
                # swallow - email may not be configured in dev
                pass

        # store email in session to continue flow (do not reveal existence)
        request.session['pw_reset_email'] = email
        return redirect(reverse('accounts-password-reset-verify'))

    return render(request, 'accounts/password_reset_request.html', ctx)


def password_reset_confirm_page(request):
    """Template view: accept OTP + new password and perform password change."""
    email = request.session.get('pw_reset_email', request.GET.get('email', ''))
    ctx = {'email': email}

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        code = request.POST.get('otp', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm = request.POST.get('confirm_password', '').strip()

        if not email or not code or not new_password or not confirm:
            ctx['error'] = 'All fields are required.'
            return render(request, 'accounts/password_reset_confirm.html', ctx)
        if new_password != confirm:
            ctx['error'] = 'Passwords do not match.'
            return render(request, 'accounts/password_reset_confirm.html', ctx)

        # find latest unused otp for this email
        otp = PasswordResetOTP.objects.filter(email=email, used=False).order_by('-created_at').first()
        if not otp:
            ctx['error'] = 'No OTP request found for this email. Please request a new code.'
            return render(request, 'accounts/password_reset_confirm.html', ctx)

        if otp.is_expired():
            ctx['error'] = 'OTP has expired. Please request a new code.'
            return render(request, 'accounts/password_reset_confirm.html', ctx)

        if otp.attempts >= 5:
            ctx['error'] = 'Maximum attempts exceeded for this OTP. Please request a new code.'
            return render(request, 'accounts/password_reset_confirm.html', ctx)

        if otp.otp_code != code:
            otp.increment_attempts()
            remaining = max(0, 5 - otp.attempts)
            ctx['error'] = f'Invalid code. Remaining attempts: {remaining}'
            return render(request, 'accounts/password_reset_confirm.html', ctx)

        # code matches
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # don't reveal; treat as success but do nothing
            request.session.pop('pw_reset_email', None)
            ctx['message'] = 'If this email exists, your password has been changed.'
            return render(request, 'accounts/password_reset_confirm.html', ctx)

        # set password
        user.set_password(new_password)
        user.save()
        Token.objects.filter(user=user).delete()
        otp.mark_used()
        request.session.pop('pw_reset_email', None)
        ctx['message'] = 'Your password has been reset successfully. You can now log in.'
        return render(request, 'accounts/password_reset_confirm.html', ctx)

    return render(request, 'accounts/password_reset_confirm.html', ctx)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password', '').strip()

        if not uidb64 or not token or not new_password:
            return Response({'error': 'uid, token and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        # optionally, invalidate existing tokens
        Token.objects.filter(user=user).delete()
        return Response({'message': 'Password has been reset successfully'})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete auth token to logout from token-based sessions
        Token.objects.filter(user=request.user).delete()
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })


# --- SPA-friendly JSON endpoints and API key protection ---
from django.http import JsonResponse





class SignupOTPRequestAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Do not reveal whether the email is already registered. If the
        # account exists, behave as if the request succeeded but don't create
    from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup_otp'
    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Do not reveal whether the email is already registered. If the
        # account exists, behave as if the request succeeded but don't create
        # an OTP. If the account does not exist, create/send an OTP as usual.
        # If the email already exists, return an explicit error per new behavior.
        if User.objects.filter(email__iexact=email).exists():
            return Response({'error': 'Sorry, user already exists'}, status=status.HTTP_409_CONFLICT)

        now = timezone.now()
        otp = SignupOTP.objects.filter(email=email, used=False).order_by('-created_at').first()
        if otp and not otp.is_expired():
            code = otp.otp_code
            expires_at = otp.expires_at
        else:
            code = f"{random.randint(100000, 999999):06d}"
            expires_at = now + timedelta(minutes=5)
            otp = SignupOTP.objects.create(email=email, otp_code=code, expires_at=expires_at)

        subject = 'Your GI Yatra signup verification code'
        message = f"Your signup verification code is: {code}\nThis code is valid for 5 minutes.\nIf you did not request this, ignore this email."
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', None))
        try:
            send_mail(subject, message, from_email, [email], fail_silently=False)
        except Exception:
            pass

        return Response({'message': 'If this email is available, a verification code was sent.'}, status=status.HTTP_200_OK)


class SignupOTPConfirmAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        code = (request.data.get('otp') or '').strip()
        password = request.data.get('password') or ''

        if not email or not code or not password:
            return Response({'error': 'email, otp and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # If a user with this email already exists, return an explicit conflict
        # so callers know the account cannot be created.
        if User.objects.filter(email__iexact=email).exists():
            return Response({'error': 'Sorry, user already exists'}, status=status.HTTP_409_CONFLICT)

        otp = SignupOTP.objects.filter(email=email, used=False).order_by('-created_at').first()
        if not otp:
            return Response({'error': 'No OTP request found'}, status=status.HTTP_400_BAD_REQUEST)
        if otp.is_blocked():
            return Response({'error': 'Too many failed attempts. Try again later.'}, status=status.HTTP_403_FORBIDDEN)
        if otp.is_expired():
            return Response({'error': 'OTP expired. Request a new code.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.otp_code != code:
            otp.increment_attempts()
            remaining = max(0, 5 - otp.attempts)
            return Response({'error': 'Invalid code', 'remaining_attempts': remaining}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        otp.mark_used()
        return Response({'message': 'Signup successful', 'token': token.key}, status=status.HTTP_201_CREATED)


class PasswordResetOTPRequestAPI(APIView):
    permission_classes = [AllowAny]

    from rest_framework.throttling import ScopedRateThrottle
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password_reset_otp'
    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # New behavior: return explicit error when email not registered
            return Response({'error': 'This email is not found in database'}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        otp = PasswordResetOTP.objects.filter(email=email, used=False).order_by('-created_at').first()
        if otp and not otp.is_expired():
            code = otp.otp_code
            expires_at = otp.expires_at
        else:
            code = f"{random.randint(100000, 999999):06d}"
            expires_at = now + timedelta(minutes=5)
            otp = PasswordResetOTP.objects.create(email=email, otp_code=code, expires_at=expires_at)

        if user:
            subject = 'Your GI Yatra password reset code'
            message = f"Your password reset code is: {code}\nThis code is valid for 5 minutes.\nIf you did not request this, ignore this email."
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', None))
            try:
                send_mail(subject, message, from_email, [email], fail_silently=False)
            except Exception:
                pass

        return Response({'message': 'If this email exists, a password reset code has been sent.', 'expires_at': expires_at})


class PasswordResetOTPConfirmAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get('email') or '').strip().lower()
        code = (request.data.get('otp') or '').strip()
        new_password = request.data.get('new_password') or ''

        if not email or not code or not new_password:
            return Response({'error': 'email, otp and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)

        otp = PasswordResetOTP.objects.filter(email=email, used=False).order_by('-created_at').first()
        if not otp:
            return Response({'error': 'No OTP request found'}, status=status.HTTP_400_BAD_REQUEST)
        if otp.attempts >= 5:
            return Response({'error': 'Maximum attempts exceeded. Request a new code.'}, status=status.HTTP_403_FORBIDDEN)
        if otp.is_expired():
            return Response({'error': 'OTP expired. Request a new code.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.otp_code != code:
            otp.increment_attempts()
            remaining = max(0, 5 - otp.attempts)
            return Response({'error': 'Invalid code', 'remaining_attempts': remaining}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            Token.objects.filter(user=user).delete()
        except User.DoesNotExist:
            pass
        otp.mark_used()
        return Response({'message': 'Password has been reset successfully'})


@ensure_csrf_cookie
def get_csrf_token(request):
    """Set and return CSRF cookie for SPA clients."""
    return JsonResponse({'detail': 'CSRF cookie set'})
