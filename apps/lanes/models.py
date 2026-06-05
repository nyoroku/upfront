from django.db import models
from django.utils import timezone
from apps.accounts.models import TimeStampedModel


class MilestoneTemplate(TimeStampedModel):
    """Admin-defined master milestone steps for each destination."""
    DESTINATION_CHOICES = [
        ('UK', 'UK'),
        ('USA', 'USA'),
        ('AU', 'Australia'),
        ('ALL', 'All'),
    ]

    destination = models.CharField(max_length=3, choices=DESTINATION_CHOICES)
    order = models.PositiveSmallIntegerField()  # 1-based sort order
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon_name = models.CharField(max_length=60)  # heroicon name
    is_free = models.BooleanField(default=False)
    required_docs = models.JSONField(default=list)
    unlock_after = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='unlocks'
    )

    class Meta:
        ordering = ['destination', 'order']
        unique_together = [['destination', 'order']]

    def __str__(self):
        return f"[{self.destination}] {self.order}. {self.title}"


class CandidateMilestone(TimeStampedModel):
    """Per-user state machine for a milestone."""
    STATUS_CHOICES = [
        ('LOCKED', 'Locked'),
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING_REVIEW', 'Pending Review'),
        ('COMPLETED', 'Completed'),
    ]

    candidate = models.ForeignKey(
        'accounts.CandidateProfile', on_delete=models.CASCADE,
        related_name='milestones'
    )
    template = models.ForeignKey(MilestoneTemplate, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LOCKED')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)  # partner reviewer notes

    class Meta:
        unique_together = [['candidate', 'template']]

    def __str__(self):
        return f"{self.candidate} — {self.template.title} ({self.status})"

    def unlock(self):
        """Transition LOCKED -> IN_PROGRESS."""
        if self.status == 'LOCKED':
            self.status = 'IN_PROGRESS'
            self.started_at = timezone.now()
            self.save(update_fields=['status', 'started_at', 'updated_at'])

    def complete(self):
        """Transition any status -> COMPLETED. Triggers next milestone unlock via signal."""
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])
