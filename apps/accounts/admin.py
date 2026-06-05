from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import CandidateProfile, PartnerProfile
from apps.lanes.models import CandidateMilestone
from apps.courses.models import CandidateProgress

TINYMCE_OVERRIDES = {models.TextField: {'widget': TinyMCE}}


class CandidateMilestoneInline(admin.TabularInline):
    model = CandidateMilestone
    extra = 0
    fields = ['template', 'status', 'started_at', 'completed_at', 'notes']
    readonly_fields = ['started_at', 'completed_at']
    autocomplete_fields = ['template']


class CandidateProgressInline(admin.TabularInline):
    model = CandidateProgress
    extra = 0
    fields = ['module', 'completed', 'watch_percent', 'completed_at']
    readonly_fields = ['completed_at']


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'destination', 'status', 'activation_rate', 'activated_at']
    list_filter = ['destination', 'status', 'qualification']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'nck_number']
    readonly_fields = ['activation_rate', 'activated_at']
    formfield_overrides = TINYMCE_OVERRIDES
    inlines = [CandidateMilestoneInline, CandidateProgressInline]


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'can_verify_docs', 'can_upload_content']
    list_filter = ['role']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
