from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DocumentType, CandidateDocument


@login_required
def vault_home(request):
    """Document vault home — list all documents for the candidate."""
    profile = request.user.profile
    documents = CandidateDocument.objects.filter(
        candidate=profile
    ).select_related('document_type').order_by('-created_at')

    # SQLite doesn't support JSONField __contains; filter in Python
    all_doc_types = DocumentType.objects.all()
    document_types = [
        dt for dt in all_doc_types
        if profile.destination in (dt.destinations or [])
    ]

    return render(request, 'vault/vault_home.html', {
        'documents': documents,
        'document_types': document_types,
        'profile': profile,
    })


@login_required
def document_upload(request):
    """Upload a document to the vault. HTMX endpoint."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    profile = request.user.profile
    doc_type_id = request.POST.get('document_type')
    uploaded_file = request.FILES.get('file')

    if not doc_type_id or not uploaded_file:
        if request.htmx:
            return render(request, 'partials/upload_error.html', {
                'error': 'Please select a document type and file.'
            })
        return HttpResponse('Missing fields', status=400)

    doc_type = get_object_or_404(DocumentType, pk=doc_type_id)

    document = CandidateDocument.objects.create(
        candidate=profile,
        document_type=doc_type,
        file=uploaded_file,
        original_filename=uploaded_file.name,
        file_size_kb=uploaded_file.size // 1024,
        verification_status='UPLOADED',
    )

    if request.htmx:
        return render(request, 'partials/document_row.html', {'doc': document})
    return HttpResponse(status=201)


@login_required
def document_delete(request, pk):
    """Delete a document from the vault. HTMX endpoint."""
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    document = get_object_or_404(
        CandidateDocument, pk=pk, candidate=request.user.profile
    )
    document.file.delete(save=False)
    document.delete()

    if request.htmx:
        return HttpResponse('')  # empty response removes the row
    return HttpResponse(status=204)
