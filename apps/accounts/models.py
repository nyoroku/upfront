import uuid
from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    """Abstract base model with UUID primary key and auto timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CandidateProfile(TimeStampedModel):
    DESTINATION_CHOICES = [
        ('UK', 'Orthopedic & Spine Care'),
        ('USA', 'Sports Rehabilitation'),
        ('AU', 'Neurological & Stroke Recovery'),
    ]
    QUALIFICATION_CHOICES = [
        ('DEGREE', 'Bachelor of Science in Physiotherapy'),
        ('DIPLOMA', 'Diploma in Physiotherapy'),
    ]
    STATUS_CHOICES = [
        ('ONBOARDING', 'Onboarding'),
        ('ACTIVE', 'Active'),
        ('PLACEMENT_READY', 'Placement Ready'),
        ('PLACED', 'Placed'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    destination = models.CharField(max_length=3, choices=DESTINATION_CHOICES)
    qualification = models.CharField(max_length=10, choices=QUALIFICATION_CHOICES)
    nck_number = models.CharField(max_length=50, blank=True, verbose_name="Physiotherapy Council Registration Number")  # e.g. PCT/12345/2026
    phone_number = models.CharField(max_length=20)  # for M-Pesa STK Push
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ONBOARDING')
    activation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    activated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Candidate Profile'
        indexes = [models.Index(fields=['destination', 'status'])]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.destination})"


class PartnerProfile(TimeStampedModel):
    ROLE_CHOICES = [
        ('MENTOR', 'UK Nursing Mentor'),
        ('THERAPIST', 'Psychotherapist'),
        ('ADMIN', 'Platform Administrator'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    can_verify_docs = models.BooleanField(default=False)
    can_upload_content = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Partner Profile'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.get_role_display()})"
