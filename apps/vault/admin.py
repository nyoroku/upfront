from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import DocumentType, CandidateDocument

TINYMCE_OVERRIDES = {models.TextField: {'widget': TinyMCE}}


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'requires_expiry']
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(CandidateDocument)
class CandidateDocumentAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'document_type', 'verification_status', 'verified_by', 'created_at']
    list_filter = ['verification_status', 'document_type']
    search_fields = ['candidate__user__email']
    readonly_fields = ['file', 'original_filename', 'file_size_kb', 'verified_at']
