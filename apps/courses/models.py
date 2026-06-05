from django.db import models
from apps.accounts.models import TimeStampedModel


class Course(TimeStampedModel):
    EXAM_TYPE_CHOICES = [
        ('NCLEX', 'NCLEX-RN (USA/AU)'),
        ('CBT', 'UK Computer Based Test'),
        ('IELTS', 'IELTS Academic'),
        ('GENERAL', 'General / Wellness'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    destination = models.CharField(max_length=3)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    description = models.TextField()
    is_free = models.BooleanField(default=False)
    milestone = models.ForeignKey(
        'lanes.MilestoneTemplate', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='courses'
    )
    total_modules = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['destination', 'title']

    def __str__(self):
        return self.title


class Module(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    order = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True)
    pdf_resource = models.FileField(upload_to='courses/pdfs/', blank=True, null=True)
    duration_minutes = models.PositiveSmallIntegerField(default=0)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} — {self.order}. {self.title}"


class Quiz(TimeStampedModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    time_limit_minutes = models.PositiveSmallIntegerField(default=60)
    pass_mark_percent = models.PositiveSmallIntegerField(default=70)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title


class Question(TimeStampedModel):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice'),
        ('NGN', 'Next Generation NCLEX — Extended Reasoning'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=5, choices=QUESTION_TYPE_CHOICES)
    body = models.TextField()
    explanation = models.TextField()
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['quiz', 'order']

    def __str__(self):
        return f"Q{self.order}: {self.body[:60]}..."


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} {self.text[:50]}"


class CandidateProgress(TimeStampedModel):
    candidate = models.ForeignKey(
        'accounts.CandidateProfile', on_delete=models.CASCADE,
        related_name='course_progress'
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    watch_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        unique_together = [['candidate', 'module']]
        verbose_name_plural = 'Candidate Progress'

    def __str__(self):
        return f"{self.candidate} — {self.module.title} ({'Done' if self.completed else f'{self.watch_percent}%'})"


class QuizAttempt(TimeStampedModel):
    candidate = models.ForeignKey(
        'accounts.CandidateProfile', on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score_percent = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=False)
    answers = models.JSONField()
    started_at = models.DateTimeField()
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidate} — {self.quiz.title}: {self.score_percent}%"
