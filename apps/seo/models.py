import uuid
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base model with UUID pk and timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ─────────────────────────────────────────────────
# Blog
# ─────────────────────────────────────────────────

class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=70, blank=True, help_text='SEO title (max 70 chars)')
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO description (max 160 chars)')

    class Meta:
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('ARCHIVED', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(max_length=300, blank=True, help_text='Short summary for cards (max 300 chars)')
    body = models.TextField(help_text='Rich text content — supports HTML')
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True, help_text='Alt text for accessibility')

    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True, help_text='SEO title tag (max 70 chars)')
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description (max 160 chars)')
    canonical_url = models.URLField(blank=True, help_text='If this post is syndicated, set canonical URL')
    og_image = models.ImageField(upload_to='blog/og/', blank=True, null=True, help_text='Open Graph image (1200x630)')

    # Relations
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    # Publishing
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    # Schema.org structured data
    reading_time_minutes = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    @property
    def seo_title(self):
        return self.meta_title or self.title

    @property
    def seo_description(self):
        return self.meta_description or self.excerpt


# ─────────────────────────────────────────────────
# FAQs
# ─────────────────────────────────────────────────

class FAQCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'
        ordering = ['order']

    def __str__(self):
        return self.name


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=300)
    answer = models.TextField(help_text='Rich text answer — supports HTML')
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    order = models.PositiveIntegerField(default=0)

    # SEO — generates FAQ schema markup
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['category__order', 'order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


# ─────────────────────────────────────────────────
# Local Pages (destination-specific SEO landing pages)
# ─────────────────────────────────────────────────

class LocalPage(TimeStampedModel):
    """
    Destination-specific landing pages for SEO.
    e.g., "Nursing Jobs in the UK", "NCLEX Prep for Kenyan Nurses"
    Equivalent to local/city pages in local SEO strategies.
    """
    DESTINATION_CHOICES = [
        ('UK', 'United Kingdom'),
        ('USA', 'United States'),
        ('AUS', 'Australia'),
        ('ALL', 'All Destinations'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    destination = models.CharField(max_length=3, choices=DESTINATION_CHOICES, default='ALL')

    # Content sections
    hero_headline = models.CharField(max_length=200)
    hero_subheadline = models.TextField(max_length=500, blank=True)
    body = models.TextField(help_text='Rich text content — supports HTML')

    # Key facts / stats section
    stat_1_label = models.CharField(max_length=50, blank=True, help_text='e.g., Average Salary')
    stat_1_value = models.CharField(max_length=50, blank=True, help_text='e.g., £35,000/yr')
    stat_2_label = models.CharField(max_length=50, blank=True)
    stat_2_value = models.CharField(max_length=50, blank=True)
    stat_3_label = models.CharField(max_length=50, blank=True)
    stat_3_value = models.CharField(max_length=50, blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='pages/og/', blank=True, null=True)

    # CTA
    cta_text = models.CharField(max_length=100, default='Start Your Journey')
    cta_url = models.CharField(max_length=200, default='/accounts/signup/')

    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['destination', 'title']

    def __str__(self):
        return f'{self.title} ({self.get_destination_display()})'

    @property
    def seo_title(self):
        return self.meta_title or self.title

    @property
    def seo_description(self):
        return self.meta_description or self.hero_subheadline


# ─────────────────────────────────────────────────
# Dynamic Homepage Models (Katrue Aesthetic)
# ─────────────────────────────────────────────────

class Testimonial(TimeStampedModel):
    """Client reviews displayed on the homepage in a Katrue-style carousel."""
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=5, help_text="e.g., 'MW' for Mary W.")
    route_from = models.CharField(max_length=100, help_text="e.g., 'Nairobi'")
    route_to = models.CharField(max_length=100, help_text="e.g., 'London'")
    content = models.TextField(help_text="The testimonial quote.")
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5 stars")
    
    # Katrue Aesthetic styling per card
    bg_color_class = models.CharField(max_length=50, default="bg-brand-100", help_text="Tailwind class like 'bg-brand-100' or 'bg-green-100'")
    text_color_class = models.CharField(max_length=50, default="text-brand-700", help_text="Tailwind class like 'text-brand-700' or 'text-green-700'")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"Testimonial: {self.name}"


class DestinationHighlight(TimeStampedModel):
    """The rich picture cards on the homepage (e.g. UK, USA, AUS)."""
    country_name = models.CharField(max_length=100)
    flag_emoji = models.CharField(max_length=10, help_text="e.g., 🇬🇧")
    badge_text = models.CharField(max_length=50, help_text="e.g., CBT + NMC")
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='home/destinations/', help_text="High-res background image")
    link_url = models.CharField(max_length=200, default="#", help_text="URL to redirect to (e.g. a local page slug)")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'country_name']
        verbose_name_plural = "Destination Highlights"

    def __str__(self):
        return self.country_name


class PathwayHighlight(TimeStampedModel):
    """The smaller localized SEO links below the main destination cards."""
    title = models.CharField(max_length=150, help_text="e.g., Nursing in London")
    subtitle = models.CharField(max_length=150, help_text="e.g., NHS Trusts & Private Care")
    link_url = models.CharField(max_length=200, default="#", help_text="URL referencing the specific LocalPage")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = "Pathway Highlights"

    def __str__(self):
        return self.title

class FooterLinkCategory(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., 'Explore', 'Resources'")
    order = models.PositiveIntegerField(default=0, help_text="Order in which categories appear (left to right)")

    class Meta:
        verbose_name_plural = "Footer Link Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class FooterLink(models.Model):
    category = models.ForeignKey(FooterLinkCategory, related_name='links', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500, help_text="Can be a URL or a named URL pattern like '/about' or 'https://...'")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    @property
    def get_url(self):
        if self.url.startswith('/') or self.url.startswith('http') or self.url == '#':
            return self.url
        try:
            from django.urls import reverse
            return reverse(self.url)
        except:
            return self.url
