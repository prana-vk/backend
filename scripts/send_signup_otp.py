import os
import django
import sys
from pathlib import Path

# Ensure project root is on sys.path so project packages can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Disable SSL redirect for this local script (so test client doesn't get 301)
os.environ.setdefault('SECURE_SSL_REDIRECT', 'False')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giyatra_project.settings')
django.setup()

from rest_framework.test import APIClient
from django.conf import settings

email = 'kp755505@gmail.com'
api_key = os.environ.get('FRONTEND_API_KEY', settings.FRONTEND_API_KEY)

print('Generating signup OTP for:', email)
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from accounts.models import SignupOTP
from django.core.mail import send_mail
from django.conf import settings

email_l = email.lower()
if User.objects.filter(email=email_l).exists():
    print('Email already registered')
    sys.exit(1)

now = timezone.now()
otp = SignupOTP.objects.filter(email=email_l, used=False).order_by('-created_at').first()
if otp and not otp.is_expired():
    code = otp.otp_code
    expires_at = otp.expires_at
else:
    code = f"{random.randint(100000, 999999):06d}"
    expires_at = now + timedelta(minutes=5)
    otp = SignupOTP.objects.create(email=email_l, otp_code=code, expires_at=expires_at)

subject = 'Your GI Yatra signup verification code'
message = f"Your signup verification code is: {code}\nThis code is valid for 5 minutes.\nIf you did not request this, ignore this email."
from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', None))
try:
    send_mail(subject, message, from_email, [email_l], fail_silently=False)
    print('Email send attempted (no exceptions).')
except Exception as e:
    print('send_mail raised exception:', repr(e))

print('Created OTP record:', otp.otp_code, 'expires_at=', otp.expires_at)
