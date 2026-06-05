from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from apps.vault.models import CandidateDocument
from .utils import _update_activation_rate, _check_milestone_doc_completion


@receiver(post_save, sender=CandidateDocument)
def on_document_upload(sender, instance, created, **kwargs):
    """Track activation: first doc upload triggers activation_rate calculation."""
    if created and instance.verification_status == 'UPLOADED':
        profile = instance.candidate
        if not profile.activated_at:
            profile.activated_at = timezone.now()
            profile.save(update_fields=['activated_at'])
        # Recalculate activation rate
        _update_activation_rate(profile)
        # Check if this document completes a milestone's required_docs
        _check_milestone_doc_completion(profile, instance.document_type.slug)
