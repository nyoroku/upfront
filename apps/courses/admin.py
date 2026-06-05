from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Course, Module, Quiz, Question, Choice, CandidateProgress, QuizAttempt

TINYMCE_OVERRIDES = {models.TextField: {'widget': TinyMCE}}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_type', 'destination', 'is_free', 'total_modules']
    list_filter = ['exam_type', 'destination', 'is_free']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'order', 'title', 'duration_minutes', 'is_preview']
    list_filter = ['course', 'is_preview']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'time_limit_minutes', 'pass_mark_percent']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'order', 'question_type', 'body']
    list_filter = ['question_type']
    inlines = [ChoiceInline]
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'quiz', 'score_percent', 'passed', 'submitted_at']
    list_filter = ['passed', 'quiz']
    readonly_fields = ['answers']
