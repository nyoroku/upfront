from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Module, CandidateProgress
from apps.lanes.models import CandidateMilestone


class CourseAccessMixin(LoginRequiredMixin):
    """Check course access: preview, paid, or milestone unlocked."""

    def dispatch(self, request, *args, **kwargs):
        module_pk = kwargs.get('pk')
        if module_pk:
            self.module = get_object_or_404(Module, pk=module_pk)
            if not self._has_access(request.user.profile):
                return redirect(
                    reverse('payments:payment_initiate')
                )
        return super().dispatch(request, *args, **kwargs)

    def _has_access(self, profile):
        if self.module.is_preview:
            return True
        if not self.module.course.milestone:
            return True  # course not gated
        milestone_status = CandidateMilestone.objects.filter(
            candidate=profile,
            template=self.module.course.milestone,
            status__in=['IN_PROGRESS', 'COMPLETED']
        ).exists()
        return milestone_status
