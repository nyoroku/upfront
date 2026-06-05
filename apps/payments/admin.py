from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import PaymentPlan, MpesaTransaction

TINYMCE_OVERRIDES = {models.TextField: {'widget': TinyMCE}}


@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount_ksh', 'unlocks_milestone']
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'plan', 'amount', 'status', 'mpesa_receipt_number', 'created_at']
    list_filter = ['status']
    search_fields = ['candidate__user__email', 'checkout_request_id', 'mpesa_receipt_number']
    readonly_fields = [
        'checkout_request_id', 'merchant_request_id', 'mpesa_receipt_number',
        'transaction_date', 'result_code', 'result_desc'
    ]
