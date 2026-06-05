from django.db import models
from apps.accounts.models import TimeStampedModel


class PaymentPlan(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    amount_ksh = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    unlocks_milestone = models.ForeignKey(
        'lanes.MilestoneTemplate', null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.name} — KSH {self.amount_ksh}"


class MpesaTransaction(TimeStampedModel):
    STATUS_CHOICES = [
        ('INITIATED', 'STK Push Initiated'),
        ('PENDING', 'Awaiting Callback'),
        ('SUCCESS', 'Payment Successful'),
        ('FAILED', 'Payment Failed'),
        ('CANCELLED', 'Cancelled by User'),
        ('TIMEOUT', 'Transaction Timed Out'),
    ]

    candidate = models.ForeignKey(
        'accounts.CandidateProfile', on_delete=models.CASCADE,
        related_name='transactions'
    )
    plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE)
    checkout_request_id = models.CharField(max_length=200, unique=True)
    merchant_request_id = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INITIATED')
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['checkout_request_id'])]

    def __str__(self):
        return f"{self.candidate} — {self.plan.name} ({self.status})"
