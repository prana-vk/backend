from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    MeView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    password_reset_page,
    password_reset_confirm_page,
    SignupOTPRequestAPI,
    SignupOTPConfirmAPI,
    PasswordResetOTPRequestAPI,
    PasswordResetOTPConfirmAPI,
    get_csrf_token,
)

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('auth/password-reset-page/', password_reset_page, name='accounts-password-reset-page'),
    path('auth/password-reset-verify/', password_reset_confirm_page, name='accounts-password-reset-verify'),
    path('auth/csrf/', get_csrf_token, name='auth-csrf'),
    # (Signup template pages removed — SPA should use API endpoints instead)
    # SPA-friendly JSON API endpoints (require X-API-KEY header if FRONTEND_API_KEY configured)
    path('auth/api/signup/request-otp/', SignupOTPRequestAPI.as_view(), name='api-signup-request-otp'),
    path('auth/api/signup/confirm-otp/', SignupOTPConfirmAPI.as_view(), name='api-signup-confirm-otp'),
    path('auth/api/password-reset/request-otp/', PasswordResetOTPRequestAPI.as_view(), name='api-password-reset-request-otp'),
    path('auth/api/password-reset/confirm-otp/', PasswordResetOTPConfirmAPI.as_view(), name='api-password-reset-confirm-otp'),
]
