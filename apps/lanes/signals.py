from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CandidateMilestone


@receiver(post_save, sender=CandidateMilestone)
def on_milestone_status_change(sender, instance, created, **kwargs):
    """When a milestone is COMPLETED, unlock the next milestone in sequence."""
    if not created and instance.status == 'COMPLETED':
        next_milestone = CandidateMilestone.objects.filter(
            candidate=instance.candidate,
            template__order=instance.template.order + 1,
            template__destination__in=[instance.candidate.destination, 'ALL'],
            status='LOCKED'
        ).first()
        if next_milestone:
            next_milestone.unlock()

        # KPI: Update candidate status if all milestones complete
        all_done = CandidateMilestone.objects.filter(
            candidate=instance.candidate
        ).exclude(status='COMPLETED').count() == 0
        if all_done:
            instance.candidate.status = 'PLACEMENT_READY'
            instance.candidate.save(update_fields=['status'])
