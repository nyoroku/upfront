import os
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.seo.models import Testimonial, DestinationHighlight, PathwayHighlight
from config.settings.base import BASE_DIR

class Command(BaseCommand):
    help = 'Seeds the database with dynamic Upfront Physiotherapy homepage content.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding dynamic homepage content for Upfront Physiotherapy...')

        # 1. Testimonials
        Testimonial.objects.all().delete()
        testimonials = [
            {
                'name': 'Mary W.',
                'initials': 'MW',
                'route_from': 'Nairobi',
                'route_to': 'Knee Rehab',
                'content': '"Dan\'s post-operative rehab was incredible. After my knee replacement, I was back on my feet and walking pain-free in just 6 weeks!"',
                'rating': 5,
                'bg_color_class': 'bg-brand-100',
                'text_color_class': 'text-brand-700',
                'order': 1
            },
            {
                'name': 'James O.',
                'initials': 'JO',
                'route_from': 'Mombasa',
                'route_to': 'Sports Injury',
                'content': '"The sports injury therapy program got me back on the rugby pitch faster than I ever expected. Professional, hands-on, and extremely knowledgeable."',
                'rating': 5,
                'bg_color_class': 'bg-green-100',
                'text_color_class': 'text-green-700',
                'order': 2
            },
            {
                'name': 'Amina N.',
                'initials': 'AN',
                'route_from': 'Kisumu',
                'route_to': 'Spine Care',
                'content': '"Struggled with chronic lower back pain for years. The personalized spine care plan and ergonomic advice completely solved it."',
                'rating': 5,
                'bg_color_class': 'bg-brand-100',
                'text_color_class': 'text-brand-700',
                'order': 3
            },
            {
                'name': 'David K.',
                'initials': 'DK',
                'route_from': 'Nakuru',
                'route_to': 'Stroke Rehab',
                'content': '"My father had a severe stroke last year. Through home-based neurological physiotherapy, his mobility and independence have improved immensely."',
                'rating': 5,
                'bg_color_class': 'bg-green-100',
                'text_color_class': 'text-green-700',
                'order': 4
            },
        ]
        
        for t_data in testimonials:
            Testimonial.objects.create(**t_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(testimonials)} testimonials.'))

        # 2. Specialty Highlights (using DestinationHighlight model)
        DestinationHighlight.objects.all().delete()
        
        destinations = [
            {
                'country_name': 'Orthopedic & Spine Care',
                'flag_emoji': '🦴',
                'badge_text': 'Orthopedics',
                'description': 'Comprehensive recovery programs for back pain, joint replacements, arthritis, and post-operative orthopedic recovery.',
                'image_filename': 'destination_uk.png',
                'order': 1
            },
            {
                'country_name': 'Sports & Active Rehab',
                'flag_emoji': '🏃‍♂️',
                'badge_text': 'Sports Rehab',
                'description': 'Targeted therapy to recover from sports injuries, restore function, prevent future re-injury, and boost athletic performance.',
                'image_filename': 'destination_us.png',
                'order': 2
            },
            {
                'country_name': 'Stroke & Neuro Care',
                'flag_emoji': '🧠',
                'badge_text': 'Neuro Rehab',
                'description': 'Specialized rehabilitation programs focusing on stroke recovery, balance restoration, and nervous system conditions.',
                'image_filename': 'destination_au.png',
                'order': 3
            }
        ]
        
        for d_data in destinations:
            img_filename = d_data.pop('image_filename')
            img_path = BASE_DIR / "static" / "images" / img_filename
            
            dest = DestinationHighlight.objects.create(**d_data)
            
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    dest.image.save(img_filename, File(f), save=True)
            else:
                self.stdout.write(self.style.WARNING(f'Image {img_filename} not found at {img_path}. Placeholder created without image.'))

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(destinations)} specialty highlights.'))

        # 3. Pathway Highlights
        PathwayHighlight.objects.all().delete()
        pathways = [
            {'title': 'Back & Neck Pain Relief', 'subtitle': 'Spine & Joint Health', 'order': 1},
            {'title': 'Post-Fracture Recovery', 'subtitle': 'Bone & Joint Rehab', 'order': 2},
            {'title': 'Stroke Rehabilitation', 'subtitle': 'Neurological Recovery', 'order': 3},
            {'title': 'Sports Injury Treatment', 'subtitle': 'Athletic Performance', 'order': 4},
            {'title': 'Ergonomic Assessment', 'subtitle': 'Occupational Health', 'order': 5},
            {'title': 'Dry Needling Therapy', 'subtitle': 'Pain Management', 'order': 6},
            {'title': 'Home Physiotherapy', 'subtitle': 'In-home Visits', 'order': 7},
        ]
        
        for p_data in pathways:
            PathwayHighlight.objects.create(**p_data)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(pathways)} pathway highlights.'))
        self.stdout.write(self.style.SUCCESS('Finished seeding dynamic homepage data.'))
