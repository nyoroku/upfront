from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import MilestoneTemplate, CandidateMilestone

TINYMCE_OVERRIDES = {models.TextField: {'widget': TinyMCE}}


@admin.register(MilestoneTemplate)
class MilestoneTemplateAdmin(admin.ModelAdmin):
    list_display = ['order', 'destination', 'title', 'is_free']
    list_display_links = ['destination', 'title']
    list_editable = ['order', 'is_free']
    list_filter = ['destination']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(CandidateMilestone)
class CandidateMilestoneAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'template', 'status', 'started_at', 'completed_at']
    list_filter = ['status', 'template__destination']
    search_fields = ['candidate__user__email', 'candidate__user__first_name']
    readonly_fields = ['started_at', 'completed_at']
    actions = ['mark_completed', 'mark_in_progress']
    formfield_overrides = TINYMCE_OVERRIDES

    @admin.action(description='Mark selected as COMPLETED')
    def mark_completed(self, request, queryset):
        for obj in queryset:
            obj.complete()

    @admin.action(description='Mark selected as IN_PROGRESS')
    def mark_in_progress(self, request, queryset):
        for obj in queryset:
            obj.unlock()
