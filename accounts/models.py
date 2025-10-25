from django.db import models
from django.utils import timezone


class LoginAttempt(models.Model):
    """Track failed login attempts per email to implement lockout"""
    email = models.EmailField(db_index=True)
    failed_attempts = models.PositiveIntegerField(default=0)
    first_failed_at = models.DateTimeField(null=True, blank=True)
    locked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["email"])]

    def reset(self):
        self.failed_attempts = 0
        self.first_failed_at = None
        self.locked_until = None
        self.save()

    def record_failure(self):
        now = timezone.now()
        if not self.first_failed_at or (now - self.first_failed_at).total_seconds() > 2 * 3600:
            # reset window
            self.failed_attempts = 1
            self.first_failed_at = now
            self.locked_until = None
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 5:
                # lock for 2 hours from first failure in window
                self.locked_until = self.first_failed_at + timezone.timedelta(hours=2)
        self.save()

    def is_locked(self):
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False


class PasswordResetOTP(models.Model):
    """One-time password records for password reset via OTP (template flow)."""
    email = models.EmailField(db_index=True)
    otp_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["email"])]

    def is_expired(self):
        return timezone.now() > self.expires_at

    def increment_attempts(self):
        self.attempts += 1
        self.save()

    def mark_used(self):
        self.used = True
        self.save()


class SignupOTP(models.Model):
    """OTP records for signup flow. Reuse the same OTP for 5 minutes from first creation.
    Enforces max 5 verification attempts and blocks further verifications for 2 hours after 5 failures.
    """
    email = models.EmailField(db_index=True)
    otp_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    first_failed_at = models.DateTimeField(null=True, blank=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["email"])]

    def is_expired(self):
        return timezone.now() > self.expires_at

    def increment_attempts(self):
        now = timezone.now()
        # mark first failure time
        if not self.first_failed_at:
            self.first_failed_at = now
        self.attempts += 1
        # block if exceeded
        if self.attempts >= 5 and self.first_failed_at:
            self.blocked_until = self.first_failed_at + timezone.timedelta(hours=2)
        self.save()

    def is_blocked(self):
        return self.blocked_until and timezone.now() < self.blocked_until

    def mark_used(self):
        self.used = True
        self.save()
