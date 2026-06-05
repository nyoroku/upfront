from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OnboardingForm
from .models import CandidateProfile


@login_required
def onboarding(request):
    """Candidate profile setup after registration/first login."""
    # If profile already exists, redirect to dashboard
    if hasattr(request.user, 'profile'):
        return redirect('lanes:lane_dashboard')

    if request.method == 'POST':
        form = OnboardingForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.status = 'ACTIVE'
            profile.save()
            messages.success(request, 'Welcome to Worklane! Your profile has been created.')
            return redirect('lanes:lane_dashboard')
    else:
        form = OnboardingForm()

    return render(request, 'accounts/onboarding.html', {'form': form})


@login_required
def profile_view(request):
    """View and edit candidate profile."""
    try:
        profile = request.user.profile
    except CandidateProfile.DoesNotExist:
        return redirect('accounts:onboarding')

    if request.method == 'POST':
        form = OnboardingForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = OnboardingForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
