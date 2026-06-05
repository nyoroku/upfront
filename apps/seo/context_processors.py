from .models import FooterLinkCategory

def footer_links(request):
    """
    Injects global footer link categories and their active links into all templates.
    """
    categories = FooterLinkCategory.objects.prefetch_related(
        'links'
    ).filter(
        links__is_active=True
    ).distinct().order_by('order')
    
    # We will let the template filter active links or we can prefetch differently if needed.
    # To keep it simple, we fetch categories.
    # Actually, a better prefetch to only get active links:
    from django.db.models import Prefetch
    from .models import FooterLink
    
    active_categories = FooterLinkCategory.objects.prefetch_related(
        Prefetch('links', queryset=FooterLink.objects.filter(is_active=True).order_by('order'))
    ).order_by('order')
    
    return {
        'footer_categories': active_categories
    }
