import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from .models import AffiliateProfile, Referral

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def capture_referral_on_signup(sender, request, user, **kwargs):
    """
    When a new user signs up via allauth, check for a referral cookie.
    If present, create a Referral record linking the new user to the affiliate.
    """
    ref_code = request.COOKIES.get('ref_code')
    if not ref_code:
        return

    try:
        affiliate = AffiliateProfile.objects.get(
            referral_code=ref_code, is_active=True
        )
    except AffiliateProfile.DoesNotExist:
        logger.warning(f'Invalid referral code in cookie: {ref_code}')
        return

    # Don't let an affiliate refer themselves
    if affiliate.user == user:
        return

    # Don't create duplicate referrals
    if Referral.objects.filter(referred_user=user).exists():
        return

    Referral.objects.create(
        affiliate=affiliate,
        referred_user=user,
        status='SIGNED_UP',
    )
    logger.info(f'Referral created: {user.email} referred by {affiliate.referral_code}')


@receiver(post_save, sender='accounts.CandidateProfile')
def link_referral_to_candidate(sender, instance, created, **kwargs):
    """
    When a CandidateProfile is created (onboarding), link the existing
    Referral record to this candidate and update status to ACTIVE.
    """
    if not created:
        return

    try:
        referral = Referral.objects.get(referred_user=instance.user, candidate__isnull=True)
        referral.candidate = instance
        referral.status = 'ACTIVE'
        referral.save(update_fields=['candidate', 'status', 'updated_at'])
        logger.info(f'Referral linked to candidate: {instance.user.email}')
    except Referral.DoesNotExist:
        pass  # Not a referred user
