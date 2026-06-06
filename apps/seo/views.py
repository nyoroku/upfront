from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import BlogPost, BlogCategory, FAQCategory, FAQ, LocalPage


def blog_list(request):
    """Blog listing page with categories and pagination."""
    posts = BlogPost.objects.filter(
        status='PUBLISHED', published_at__lte=timezone.now()
    ).select_related('category', 'author')

    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    categories = BlogCategory.objects.all()
    featured = posts.filter(is_featured=True).first()

    return render(request, 'seo/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'featured': featured,
        'current_category': category_slug,
    })


def blog_detail(request, slug):
    """Blog post detail with structured data."""
    post = get_object_or_404(
        BlogPost, slug=slug, status='PUBLISHED'
    )
    related = BlogPost.objects.filter(
        category=post.category, status='PUBLISHED'
    ).exclude(pk=post.pk)[:3]

    return render(request, 'seo/blog_detail.html', {
        'post': post,
        'related': related,
    })


def faq_list(request):
    """FAQ page with accordion grouped by category — generates FAQ schema."""
    categories = FAQCategory.objects.prefetch_related('faqs').all()
    all_faqs = FAQ.objects.filter(is_published=True).select_related('category')

    return render(request, 'seo/faq_list.html', {
        'categories': categories,
        'all_faqs': all_faqs,
    })


def local_page_detail(request, slug):
    """Destination-specific landing page."""
    page = get_object_or_404(LocalPage, slug=slug, is_published=True)
    return render(request, 'seo/local_page.html', {'page': page})


def local_page_list(request):
    """List all destination landing pages."""
    pages = LocalPage.objects.filter(is_published=True)
    return render(request, 'seo/local_page_list.html', {'pages': pages})


def local_page_list_by_destination(request, destination):
    """List service landing pages filtered by specialty code (UK, USA, AUS)."""
    destination = destination.upper()
    dest_map = {
        'UK': 'Orthopedic & Spine Care',
        'USA': 'Sports Rehabilitation',
        'AUS': 'Neurological & Stroke Recovery'
    }
    dest_name = dest_map.get(destination, destination)
    pages = LocalPage.objects.filter(is_published=True, destination=destination)
    return render(request, 'seo/local_page_list.html', {
        'pages': pages,
        'destination_name': dest_name,
    })


def home_view(request):
    """Dynamic homepage view."""
    from .models import DestinationHighlight, PathwayHighlight, Testimonial
    
    destinations = DestinationHighlight.objects.filter(is_active=True)
    pathways = PathwayHighlight.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Grab the top 5 FAQs for the homepage
    faqs = FAQ.objects.filter(is_published=True)[:5]
    
    context = {
        'destinations': destinations,
        'pathways': pathways,
        'testimonials': testimonials,
        'faqs': faqs,
    }
    return render(request, 'pages/home.html', context)
