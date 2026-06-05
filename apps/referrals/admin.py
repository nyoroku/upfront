from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import AffiliateProfile, Referral, Commission


@admin.register(AffiliateProfile)
class AffiliateProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'referral_code', 'commission_type', 'commission_rate',
        'total_earned', 'total_paid', 'is_active', 'created_at',
    ]
    list_filter = ['commission_type', 'is_active']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'referral_code']
    readonly_fields = ['referral_code', 'total_earned', 'total_paid', 'created_at']
    list_editable = ['commission_type', 'commission_rate', 'is_active']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = [
        'referred_user', 'affiliate', 'candidate', 'status', 'created_at',
    ]
    list_filter = ['status']
    search_fields = [
        'referred_user__email', 'affiliate__referral_code',
        'affiliate__user__email',
    ]
    readonly_fields = ['created_at']
    raw_id_fields = ['referred_user', 'affiliate', 'candidate']


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = [
        'referral', 'amount', 'status', 'transaction', 'paid_at', 'created_at',
    ]
    list_filter = ['status']
    search_fields = [
        'referral__affiliate__referral_code',
        'referral__referred_user__email',
        'transaction__mpesa_receipt_number',
    ]
    readonly_fields = ['referral', 'transaction', 'amount', 'created_at']
    list_editable = ['status']
    actions = ['mark_as_paid']

    @admin.action(description='Mark selected commissions as Paid')
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status__in=['PENDING', 'APPROVED']).update(
            status='PAID', paid_at=timezone.now()
        )
        self.message_user(request, f'{updated} commission(s) marked as paid.')
