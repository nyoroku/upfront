"""
Management command to seed placeholder data for the new Footer models.
Run with: python manage.py seed_footer
"""

import sys
from django.core.management.base import BaseCommand
from apps.seo.models import FooterLinkCategory, FooterLink

class Command(BaseCommand):
    help = 'Seeds initial footer layout data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to seed footer links...")

        # Clear existing data first to avoid duplicates on multiple runs
        FooterLink.objects.all().delete()
        FooterLinkCategory.objects.all().delete()

        # Define the categories
        categories_data = [
            {'name': 'Explore', 'order': 1},
            {'name': 'Specialties', 'order': 2},
            {'name': 'Resources', 'order': 3},
            {'name': 'Company', 'order': 4},
        ]

        categories = {}
        for cat_data in categories_data:
            cat = FooterLinkCategory.objects.create(**cat_data)
            categories[cat.name] = cat
            self.stdout.write(f"Created category: {cat.name}")

        # Define the links for each category
        links_data = [
            # Explore
            {'category': categories['Explore'], 'title': 'Home', 'url': 'home', 'order': 1},
            {'category': categories['Explore'], 'title': 'Journal', 'url': 'seo:blog_list', 'order': 2},
            {'category': categories['Explore'], 'title': 'FAQ', 'url': 'seo:faq_list', 'order': 3},
            {'category': categories['Explore'], 'title': 'Our Services', 'url': 'seo:local_page_list', 'order': 4},

            # Specialties
            {'category': categories['Specialties'], 'title': '🦴 Orthopedic Care', 'url': '#', 'order': 1},
            {'category': categories['Specialties'], 'title': '🏃 Sports Rehabilitation', 'url': '#', 'order': 2},
            {'category': categories['Specialties'], 'title': '🧠 Neurological Rehab', 'url': '#', 'order': 3},

            # Resources
            {'category': categories['Resources'], 'title': 'Back Pain Guide', 'url': '#', 'order': 1},
            {'category': categories['Resources'], 'title': 'Ergonomic Tips', 'url': '#', 'order': 2},
            {'category': categories['Resources'], 'title': 'Stroke Recovery', 'url': '#', 'order': 3},
            {'category': categories['Resources'], 'title': 'Post-Surgery Rehab', 'url': '#', 'order': 4},

            # Company
            {'category': categories['Company'], 'title': 'About Dan Gichobi', 'url': '#', 'order': 1},
            {'category': categories['Company'], 'title': 'Contact', 'url': '#', 'order': 2},
            {'category': categories['Company'], 'title': 'Privacy Policy', 'url': '#', 'order': 3},
            {'category': categories['Company'], 'title': 'Terms of Service', 'url': '#', 'order': 4},
        ]

        for link_data in links_data:
            link = FooterLink.objects.create(**link_data)
            self.stdout.write(f"Created link under {link.category.name}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded footer links.'))
