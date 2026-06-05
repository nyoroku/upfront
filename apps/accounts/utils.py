from apps.vault.models import DocumentType, CandidateDocument
from apps.lanes.models import CandidateMilestone


def _update_activation_rate(profile):
    """
    Activation Rate = (profile_fields_complete + docs_uploaded) / total_required
    Stored as a percentage (0-100).
    """
    profile_fields = ['destination', 'qualification', 'nck_number', 'phone_number', 'profile_photo']
    profile_score = sum(1 for f in profile_fields if getattr(profile, f)) / len(profile_fields)

    required_docs = DocumentType.objects.filter(
        destinations__contains=profile.destination
    ).count()
    uploaded_docs = CandidateDocument.objects.filter(
        candidate=profile,
        verification_status__in=['UPLOADED', 'APPROVED']
    ).count()
    doc_score = (uploaded_docs / required_docs) if required_docs else 0

    profile.activation_rate = ((profile_score + doc_score) / 2) * 100
    profile.save(update_fields=['activation_rate'])


def _check_milestone_doc_completion(profile, doc_slug):
    """
    Check if uploading this document completes a milestone's required_docs list.
    If all required docs are uploaded/approved, transition milestone to PENDING_REVIEW.
    """
    # Find milestones that require this document
    milestones = CandidateMilestone.objects.filter(
        candidate=profile,
        status='IN_PROGRESS',
        template__required_docs__contains=[doc_slug]
    ).select_related('template')

    for milestone in milestones:
        required_slugs = milestone.template.required_docs
        uploaded_slugs = set(
            CandidateDocument.objects.filter(
                candidate=profile,
                verification_status__in=['UPLOADED', 'APPROVED'],
                document_type__slug__in=required_slugs
            ).values_list('document_type__slug', flat=True)
        )
        if set(required_slugs).issubset(uploaded_slugs):
            milestone.status = 'PENDING_REVIEW'
            milestone.save(update_fields=['status', 'updated_at'])
