from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Sum, Count
from .models import AffiliateProfile, Referral, Commission
from .forms import AffiliateSignupForm

User = get_user_model()


def referral_redirect(request, code):
    """
    Public referral link. Sets a cookie with the referral code
    and redirects to the nurse signup page.
    """
    response = HttpResponseRedirect('/accounts/signup/')
    # Set cookie valid for 30 days
    response.set_cookie('ref_code', code, max_age=30 * 24 * 60 * 60, httponly=True)
    return response


def affiliate_signup(request):
    """Separate registration for affiliates."""
    if request.user.is_authenticated:
        if hasattr(request.user, 'affiliate_profile'):
            return redirect('referrals:affiliate_dashboard')
        messages.info(request, 'You are already logged in.')
        return redirect('home')

    if request.method == 'POST':
        form = AffiliateSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            AffiliateProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
            )
            # Auto-login
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Welcome! Your affiliate account is ready.')
            return redirect('referrals:affiliate_dashboard')
    else:
        form = AffiliateSignupForm()

    return render(request, 'referrals/signup.html', {'form': form})


def affiliate_login(request):
    """Login page for affiliates."""
    if request.user.is_authenticated:
        if hasattr(request.user, 'affiliate_profile'):
            return redirect('referrals:affiliate_dashboard')
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user and hasattr(user, 'affiliate_profile'):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('referrals:affiliate_dashboard')
        else:
            messages.error(request, 'Invalid affiliate credentials.')

    return render(request, 'referrals/login.html')


@login_required
def affiliate_dashboard(request):
    """Affiliate dashboard with stats and commission history."""
    if not hasattr(request.user, 'affiliate_profile'):
        messages.error(request, 'You do not have an affiliate account.')
        return redirect('home')

    affiliate = request.user.affiliate_profile

    # Stats
    referrals = Referral.objects.filter(affiliate=affiliate).select_related(
        'referred_user', 'candidate'
    ).order_by('-created_at')

    commissions = Commission.objects.filter(
        referral__affiliate=affiliate
    ).select_related('referral__referred_user', 'transaction').order_by('-created_at')

    stats = {
        'total_referrals': referrals.count(),
        'active_referrals': referrals.filter(status__in=['ACTIVE', 'PAID']).count(),
        'total_earned': affiliate.total_earned,
        'total_paid': affiliate.total_paid,
        'balance': affiliate.balance,
        'pending_commissions': commissions.filter(status='PENDING').aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }

    # Build referral link
    referral_url = request.build_absolute_uri(f'/ref/{affiliate.referral_code}/')

    return render(request, 'referrals/dashboard.html', {
        'affiliate': affiliate,
        'referrals': referrals[:50],
        'commissions': commissions[:50],
        'stats': stats,
        'referral_url': referral_url,
    })
