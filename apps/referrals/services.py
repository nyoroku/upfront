import logging
from decimal import Decimal
from .models import Referral, Commission

logger = logging.getLogger(__name__)


def credit_commission(txn):
    """
    Called after a successful M-Pesa payment.
    Checks if the paying candidate was referred, and if so, creates a Commission.
    """
    try:
        # Find if this candidate has a referral record
        referral = Referral.objects.select_related('affiliate').filter(
            candidate=txn.candidate
        ).first()

        if not referral:
            return  # Not a referred nurse

        if not referral.affiliate.is_active:
            logger.info(f'Affiliate {referral.affiliate.referral_code} is inactive, skipping commission.')
            return

        # Prevent double-crediting the same transaction
        if Commission.objects.filter(transaction=txn).exists():
            logger.warning(f'Commission already exists for transaction {txn.pk}')
            return

        # Calculate commission
        affiliate = referral.affiliate
        if affiliate.commission_type == 'FIXED':
            amount = affiliate.commission_rate
        else:  # PERCENTAGE
            amount = (affiliate.commission_rate / Decimal('100')) * txn.amount

        # Round to 2 decimal places
        amount = amount.quantize(Decimal('0.01'))

        # Create commission
        Commission.objects.create(
            referral=referral,
            transaction=txn,
            amount=amount,
            status='PENDING',
        )

        # Update affiliate totals
        affiliate.total_earned += amount
        affiliate.save(update_fields=['total_earned', 'updated_at'])

        # Update referral status
        if referral.status != 'PAID':
            referral.status = 'PAID'
            referral.save(update_fields=['status', 'updated_at'])

        logger.info(
            f'Commission of KSH {amount} credited to affiliate '
            f'{affiliate.referral_code} for transaction {txn.pk}'
        )

    except Exception as e:
        logger.exception(f'Error crediting commission: {e}')
