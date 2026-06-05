import uuid
import string
import random
from django.db import models
from django.conf import settings
from apps.accounts.models import TimeStampedModel


def generate_referral_code():
    """Generate a unique 8-character alphanumeric referral code."""
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=8))
        if not AffiliateProfile.objects.filter(referral_code=code).exists():
            return code


class AffiliateProfile(TimeStampedModel):
    """
    Separate profile for referral affiliates.
    Affiliates are NOT nurses — they join via a dedicated signup flow.
    """
    COMMISSION_TYPE_CHOICES = [
        ('FIXED', 'Fixed Amount (KSH)'),
        ('PERCENTAGE', 'Percentage of Payment'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='affiliate_profile',
    )
    referral_code = models.CharField(
        max_length=12, unique=True, default=generate_referral_code,
        help_text='Unique code used in referral links.',
    )
    commission_type = models.CharField(
        max_length=12, choices=COMMISSION_TYPE_CHOICES, default='FIXED',
    )
    commission_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=500.00,
        help_text='Fixed KSH amount or percentage (e.g. 500 or 10.00).',
    )
    phone_number = models.CharField(
        max_length=20, blank=True,
        help_text='Phone number for M-Pesa payouts.',
    )
    total_earned = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00,
    )
    total_paid = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Affiliate'
        verbose_name_plural = 'Affiliates'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.referral_code})"

    @property
    def balance(self):
        return self.total_earned - self.total_paid

    @property
    def referral_count(self):
        return self.referrals.count()

    @property
    def paid_referral_count(self):
        return self.referrals.filter(status='PAID').count()


class Referral(TimeStampedModel):
    """
    Tracks which nurse was referred by which affiliate.
    One nurse can only be referred by one affiliate (OneToOne on candidate).
    """
    STATUS_CHOICES = [
        ('SIGNED_UP', 'Signed Up'),
        ('ACTIVE', 'Active (Profile Created)'),
        ('PAID', 'Has Made a Payment'),
    ]

    affiliate = models.ForeignKey(
        AffiliateProfile, on_delete=models.CASCADE, related_name='referrals',
    )
    candidate = models.OneToOneField(
        'accounts.CandidateProfile', on_delete=models.CASCADE,
        related_name='referral', null=True, blank=True,
    )
    referred_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='referral_record',
        help_text='The user who signed up via referral link.',
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='SIGNED_UP',
    )

    class Meta:
        verbose_name = 'Referral'

    def __str__(self):
        return f"{self.referred_user.email} → {self.affiliate.referral_code}"


class Commission(TimeStampedModel):
    """
    One commission per successful payment from a referred nurse.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid Out'),
    ]

    referral = models.ForeignKey(
        Referral, on_delete=models.CASCADE, related_name='commissions',
    )
    transaction = models.OneToOneField(
        'payments.MpesaTransaction', on_delete=models.CASCADE,
        related_name='commission',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='PENDING',
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Commission'

    def __str__(self):
        return f"KSH {self.amount} — {self.referral.affiliate.referral_code} ({self.status})"
