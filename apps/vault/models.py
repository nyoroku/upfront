from django.db import models
from apps.accounts.models import TimeStampedModel


class DocumentType(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    requires_expiry = models.BooleanField(default=False)
    destinations = models.JSONField(default=list)

    def __str__(self):
        return self.name


class CandidateDocument(TimeStampedModel):
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending Upload'),
        ('UPLOADED', 'Uploaded — Awaiting Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected — Resubmit'),
    ]

    candidate = models.ForeignKey(
        'accounts.CandidateProfile', on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    file = models.FileField(upload_to='vault/%Y/%m/')
    original_filename = models.CharField(max_length=255)
    file_size_kb = models.PositiveIntegerField()
    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_STATUS, default='PENDING'
    )
    verified_by = models.ForeignKey(
        'accounts.PartnerProfile', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['candidate', 'verification_status'])]

    def __str__(self):
        return f"{self.candidate} — {self.document_type.name} ({self.verification_status})"
