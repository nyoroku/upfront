from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Course, Module, Quiz, CandidateProgress, QuizAttempt


@login_required
def course_list(request):
    """List all courses, optionally filtered by destination."""
    profile = request.user.profile
    courses = Course.objects.filter(
        destination__in=[profile.destination, 'ALL']
    ).order_by('title')

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'profile': profile,
    })


@login_required
def course_detail(request, slug):
    """Show course detail with modules list."""
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.order_by('order')
    profile = request.user.profile

    # Get progress for each module
    progress_map = {}
    for p in CandidateProgress.objects.filter(candidate=profile, module__course=course):
        progress_map[p.module_id] = p

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'progress_map': progress_map,
        'profile': profile,
    })


@login_required
def module_complete(request, slug, pk):
    """Mark a module as completed. HTMX endpoint."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    module = get_object_or_404(Module, pk=pk)
    profile = request.user.profile

    progress, created = CandidateProgress.objects.get_or_create(
        candidate=profile, module=module,
        defaults={'completed': True, 'completed_at': timezone.now(), 'watch_percent': 100}
    )
    if not created and not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.watch_percent = 100
        progress.save(update_fields=['completed', 'completed_at', 'watch_percent', 'updated_at'])

    # Calculate overall course progress
    total = module.course.modules.count()
    completed = CandidateProgress.objects.filter(
        candidate=profile, module__course=module.course, completed=True
    ).count()
    completion_percent = round((completed / total) * 100) if total else 0

    if request.htmx:
        return render(request, 'partials/course_progress_bar.html', {
            'completion_percent': completion_percent,
            'completed': completed,
            'total': total,
        })
    return redirect('courses:course_detail', slug=slug)


@login_required
def quiz_start(request, slug, pk):
    """Start a quiz — render quiz form with timer."""
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.prefetch_related('choices').order_by('order')

    # Store quiz start time in session
    request.session[f'quiz_{pk}_start'] = timezone.now().isoformat()

    return render(request, 'courses/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'course_slug': slug,
    })


@login_required
def quiz_submit(request, slug, pk):
    """Submit quiz answers, calculate score, return results."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    quiz = get_object_or_404(Quiz, pk=pk)
    answers = {}
    score = 0
    total = quiz.questions.count()

    for question in quiz.questions.prefetch_related('choices').all():
        submitted_choice_id = request.POST.get(f'q_{question.pk}')
        answers[str(question.pk)] = submitted_choice_id
        if submitted_choice_id and question.choices.filter(
            pk=submitted_choice_id, is_correct=True
        ).exists():
            score += 1

    score_percent = (score / total) * 100 if total else 0
    passed = score_percent >= quiz.pass_mark_percent

    # Get start time from session
    started_str = request.session.pop(f'quiz_{pk}_start', None)
    started_at = timezone.datetime.fromisoformat(started_str) if started_str else timezone.now()

    attempt = QuizAttempt.objects.create(
        candidate=request.user.profile,
        quiz=quiz,
        score_percent=score_percent,
        passed=passed,
        answers=answers,
        started_at=started_at,
        submitted_at=timezone.now()
    )

    context = {
        'attempt': attempt,
        'quiz': quiz,
        'score': score,
        'total': total,
        'course_slug': slug,
    }

    if request.htmx:
        return render(request, 'partials/quiz_results.html', context)
    return render(request, 'courses/quiz_results.html', context)
