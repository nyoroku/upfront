from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import (
    BlogCategory, BlogPost, FAQCategory, FAQ, LocalPage,
    Testimonial, DestinationHighlight, PathwayHighlight,
    FooterLinkCategory, FooterLink
)

TINYMCE_OVERRIDES = {models.TextField: {'widget': TinyMCE}}


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ['order', 'question', 'answer', 'is_published']


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'published_at']
    list_filter = ['status', 'category', 'is_featured']
    search_fields = ['title', 'excerpt', 'body']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    formfield_overrides = TINYMCE_OVERRIDES
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'category', 'author', 'status', 'published_at', 'is_featured')}),
        ('Content', {'fields': ('excerpt', 'body', 'featured_image', 'featured_image_alt', 'reading_time_minutes')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'canonical_url', 'og_image'), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FAQInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_published']
    list_filter = ['category', 'is_published']
    list_editable = ['order', 'is_published']
    list_display_links = ['question']
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(LocalPage)
class LocalPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'is_published']
    list_filter = ['destination', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = TINYMCE_OVERRIDES
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'destination', 'is_published')}),
        ('Hero', {'fields': ('hero_headline', 'hero_subheadline')}),
        ('Content', {'fields': ('body',)}),
        ('Stats', {'fields': (
            ('stat_1_label', 'stat_1_value'),
            ('stat_2_label', 'stat_2_value'),
            ('stat_3_label', 'stat_3_value'),
        )}),
        ('CTA', {'fields': ('cta_text', 'cta_url')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'og_image'), 'classes': ('collapse',)}),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'route_from', 'route_to', 'rating', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'rating']
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(DestinationHighlight)
class DestinationHighlightAdmin(admin.ModelAdmin):
    list_display = ['country_name', 'badge_text', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    formfield_overrides = TINYMCE_OVERRIDES


@admin.register(PathwayHighlight)
class PathwayHighlightAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1


@admin.register(FooterLinkCategory)
class FooterLinkCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    inlines = [FooterLinkInline]


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['category', 'is_active']

