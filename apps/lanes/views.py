from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.utils import timezone
from .models import MilestoneTemplate, CandidateMilestone


@login_required
def lane_dashboard(request):
    """Main dashboard view showing the candidate's relocation lane."""
    profile = request.user.profile
    milestones = CandidateMilestone.objects.filter(
        candidate=profile
    ).select_related('template').order_by('template__order')

    # If no milestones exist yet (new user), generate from templates
    if not milestones.exists():
        _generate_candidate_lane(profile)
        milestones = CandidateMilestone.objects.filter(
            candidate=profile
        ).select_related('template').order_by('template__order')

    context = {
        'milestones': milestones,
        'active_milestone': milestones.filter(status='IN_PROGRESS').first(),
        'completion_percent': _calculate_completion(milestones),
        'profile': profile,
    }
    return render(request, 'lanes/dashboard.html', context)


@login_required
def milestone_detail(request, slug):
    """Detailed view for a single milestone."""
    milestone = get_object_or_404(
        CandidateMilestone,
        template__slug=slug,
        candidate=request.user.profile
    )
    return render(request, 'lanes/milestone_detail.html', {'milestone': milestone})


@login_required
def milestone_status(request, slug):
    """HTMX endpoint: returns updated status badge HTML fragment only."""
    milestone = get_object_or_404(
        CandidateMilestone,
        template__slug=slug,
        candidate=request.user.profile
    )
    if not request.htmx:
        return HttpResponseBadRequest('HTMX request required')
    return render(request, 'partials/milestone_badge.html', {'milestone': milestone})


def _generate_candidate_lane(profile):
    """Create CandidateMilestone rows from MilestoneTemplate for user destination."""
    templates = MilestoneTemplate.objects.filter(
        destination__in=[profile.destination, 'ALL']
    ).order_by('order')

    milestones = []
    for i, template in enumerate(templates):
        status = 'IN_PROGRESS' if i == 0 else 'LOCKED'
        milestones.append(CandidateMilestone(
            candidate=profile,
            template=template,
            status=status,
            started_at=timezone.now() if i == 0 else None
        ))
    CandidateMilestone.objects.bulk_create(milestones)


def _calculate_completion(milestones):
    """Calculate completion percentage of milestones."""
    total = milestones.count()
    if total == 0:
        return 0
    completed = milestones.filter(status='COMPLETED').count()
    return round((completed / total) * 100)
