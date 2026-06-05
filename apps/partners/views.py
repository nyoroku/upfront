from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from apps.vault.models import CandidateDocument
from apps.accounts.models import PartnerProfile


@login_required
def partner_dashboard(request):
    """Partner admin dashboard."""
    try:
        partner = request.user.partner_profile
    except PartnerProfile.DoesNotExist:
        return HttpResponseForbidden('Partner access required.')

    # Documents pending review
    pending_docs = CandidateDocument.objects.filter(
        verification_status='UPLOADED'
    ).select_related('candidate', 'document_type').order_by('-created_at')

    return render(request, 'partners/dashboard.html', {
        'partner': partner,
        'pending_docs': pending_docs,
    })


@login_required
def verify_document(request, doc_pk):
    """Approve or reject a candidate document. HTMX endpoint."""
    try:
        partner = request.user.partner_profile
    except PartnerProfile.DoesNotExist:
        return HttpResponseForbidden('Partner access required.')

    if not partner.can_verify_docs:
        return HttpResponseForbidden('Verification permission required.')

    if request.method != 'POST':
        return HttpResponse(status=405)

    document = get_object_or_404(CandidateDocument, pk=doc_pk)
    action = request.POST.get('action')

    if action == 'approve':
        document.verification_status = 'APPROVED'
        document.verified_by = partner
        document.verified_at = timezone.now()
        document.save(update_fields=['verification_status', 'verified_by', 'verified_at', 'updated_at'])
    elif action == 'reject':
        document.verification_status = 'REJECTED'
        document.verified_by = partner
        document.verified_at = timezone.now()
        document.rejection_reason = request.POST.get('reason', '')
        document.save(update_fields=[
            'verification_status', 'verified_by', 'verified_at', 'rejection_reason', 'updated_at'
        ])

    if request.htmx:
        return render(request, 'partials/document_row.html', {'doc': document})
    return HttpResponse(status=200)
