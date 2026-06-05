import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from .models import PaymentPlan, MpesaTransaction
from .services import MpesaService
from apps.lanes.models import CandidateMilestone

logger = logging.getLogger(__name__)


@login_required
def payment_checkout(request, slug):
    """Payment checkout page for a plan."""
    plan = get_object_or_404(PaymentPlan, slug=slug)
    return render(request, 'payments/checkout.html', {
        'plan': plan,
        'profile': request.user.profile,
    })


@login_required
@require_POST
def payment_initiate(request):
    """Initiate M-Pesa STK Push. HTMX endpoint."""
    plan_slug = request.POST.get('plan_slug')
    plan = get_object_or_404(PaymentPlan, slug=plan_slug)
    profile = request.user.profile
    phone = profile.phone_number

    service = MpesaService()
    try:
        response = service.initiate_stk_push(
            phone=phone,
            amount=int(plan.amount_ksh),
            account_ref=f'WL-{profile.pk.hex[:8].upper()}',
            description=plan.name
        )
    except Exception as e:
        logger.exception(f'M-Pesa STK Push failed: {e}')
        if request.htmx:
            return render(request, 'partials/payment_error.html', {'error': str(e)})
        messages.error(request, f'Payment initiation failed: {e}')
        return redirect('payments:payment_checkout', slug=plan_slug)

    transaction = MpesaTransaction.objects.create(
        candidate=profile,
        plan=plan,
        checkout_request_id=response['CheckoutRequestID'],
        merchant_request_id=response['MerchantRequestID'],
        amount=plan.amount_ksh,
        phone_number=phone,
        status='PENDING'
    )

    if request.htmx:
        return render(request, 'partials/payment_pending.html', {'transaction': transaction})
    return redirect('payments:payment_status', pk=transaction.pk)


@csrf_exempt
@require_POST
def mpesa_callback(request):
    """Safaricom posts callback here. Process and unlock milestone."""
    try:
        data = json.loads(request.body)
        body = data['Body']['stkCallback']
        checkout_id = body['CheckoutRequestID']
        result_code = body['ResultCode']

        txn = MpesaTransaction.objects.get(checkout_request_id=checkout_id)

        if result_code == 0:  # Success
            items = {i['Name']: i.get('Value') for i in body['CallbackMetadata']['Item']}
            txn.status = 'SUCCESS'
            txn.mpesa_receipt_number = items.get('MpesaReceiptNumber', '')
            txn.transaction_date = timezone.now()
            txn.result_code = 0
            txn.save()
            _unlock_milestone_for_transaction(txn)
            # Credit affiliate commission if this nurse was referred
            from apps.referrals.services import credit_commission
            credit_commission(txn)
        else:
            txn.status = 'FAILED'
            txn.result_code = result_code
            txn.result_desc = body.get('ResultDesc', '')
            txn.save()

    except Exception as e:
        logger.exception(f'M-Pesa callback error: {e}')

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})


@login_required
def payment_status_poll(request, pk):
    """HTMX polling endpoint for payment status."""
    transaction = get_object_or_404(
        MpesaTransaction, pk=pk, candidate=request.user.profile
    )

    if transaction.status == 'SUCCESS':
        template = 'partials/payment_success.html'
    elif transaction.status in ('FAILED', 'CANCELLED', 'TIMEOUT'):
        template = 'partials/payment_error.html'
    else:
        template = 'partials/payment_pending.html'

    return render(request, template, {'transaction': transaction})


@login_required
def payment_status(request, pk):
    """Full page payment status."""
    transaction = get_object_or_404(
        MpesaTransaction, pk=pk, candidate=request.user.profile
    )
    return render(request, 'payments/status.html', {'transaction': transaction})


def _unlock_milestone_for_transaction(txn):
    """Unlock the milestone associated with the payment plan."""
    if txn.plan.unlocks_milestone:
        milestone, _ = CandidateMilestone.objects.get_or_create(
            candidate=txn.candidate,
            template=txn.plan.unlocks_milestone
        )
        milestone.unlock()
