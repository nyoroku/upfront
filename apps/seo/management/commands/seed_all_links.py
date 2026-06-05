"""
Management command to create LocalPages and fix ALL '#' links across the site.
Run with: python manage.py seed_all_links
"""
from django.core.management.base import BaseCommand
from apps.seo.models import (
    LocalPage, DestinationHighlight, PathwayHighlight,
    FooterLinkCategory, FooterLink
)


class Command(BaseCommand):
    help = 'Creates real LocalPages and updates all links to point to actual pages'

    def handle(self, *args, **kwargs):
        self.stdout.write("=== Creating LocalPages ===")
        self._create_local_pages()
        self.stdout.write("=== Updating DestinationHighlight links ===")
        self._update_destination_links()
        self.stdout.write("=== Updating PathwayHighlight links ===")
        self._update_pathway_links()
        self.stdout.write("=== Updating Footer links ===")
        self._update_footer_links()
        self.stdout.write(self.style.SUCCESS('All links updated successfully!'))

    def _create_local_pages(self):
        """Create actual LocalPage entries for each physiotherapy specialty/service."""
        pages_data = [
            # UK → Orthopedic & Spine Care
            {
                'title': 'Orthopedic Care',
                'slug': 'orthopedic-care',
                'destination': 'UK',
                'hero_headline': 'Orthopedic & Spine Care',
                'hero_subheadline': 'Personalized treatment for back pain, joint disorders, and musculoskeletal conditions.',
                'body': '<p>Our <strong>Orthopedic & Spine Care</strong> program focuses on restoring mobility and eliminating pain through evidence-based manual therapy, therapeutic exercise, and patient education.</p><h3>Conditions We Treat</h3><ul><li>Chronic lower back pain & sciatica</li><li>Cervical (neck) pain & stiffness</li><li>Shoulder impingement & frozen shoulder</li><li>Knee osteoarthritis</li><li>Post-surgical joint rehabilitation</li></ul><h3>Our Approach</h3><p>Certified physiotherapist Dan Mwangi Gichobi uses a combination of joint mobilization, myofascial release, core stabilization exercises, and posture correction to achieve lasting results. Every treatment plan is tailored to your unique condition and goals.</p>',
                'stat_1_label': 'Patients Treated', 'stat_1_value': '800+',
                'stat_2_label': 'Recovery Rate', 'stat_2_value': '96%',
                'stat_3_label': 'Avg. Program', 'stat_3_value': '6-8 weeks',
            },
            {
                'title': 'Back Pain Clinic',
                'slug': 'back-pain-clinic',
                'destination': 'UK',
                'hero_headline': 'Specialized Back Pain Clinic',
                'hero_subheadline': 'Evidence-based treatment for acute and chronic back pain conditions.',
                'body': '<p>Lower back pain is the leading cause of disability worldwide. Our dedicated <strong>Back Pain Clinic</strong> provides structured rehabilitation combining manual therapy, targeted strengthening, and lifestyle modification.</p><h3>Treatment Methods</h3><ul><li>Spinal mobilization & manipulation</li><li>McKenzie method assessment</li><li>Core stability programming</li><li>Ergonomic & posture evaluation</li></ul>',
                'stat_1_label': 'Success Rate', 'stat_1_value': '94%',
                'stat_2_label': 'Conditions', 'stat_2_value': '15+',
                'stat_3_label': 'Sessions', 'stat_3_value': '6-12',
            },
            {
                'title': 'Post-Surgical Rehabilitation',
                'slug': 'post-surgical-rehab',
                'destination': 'UK',
                'hero_headline': 'Post-Surgical Rehabilitation',
                'hero_subheadline': 'Structured recovery programs after orthopedic and joint replacement surgeries.',
                'body': '<p>After surgery, optimal recovery depends on timely and structured physical rehabilitation. Our <strong>Post-Surgical Rehab</strong> program covers joint replacements, ligament reconstructions, and spinal surgeries.</p><h3>Programs Available</h3><ul><li>Total knee replacement rehab</li><li>Total hip replacement rehab</li><li>ACL reconstruction recovery</li><li>Rotator cuff repair rehab</li><li>Spinal fusion rehabilitation</li></ul>',
                'stat_1_label': 'Surgeries Covered', 'stat_1_value': '12+',
                'stat_2_label': 'Recovery Rate', 'stat_2_value': '97%',
                'stat_3_label': 'Home Visits', 'stat_3_value': 'Available',
            },
            # USA → Sports Rehabilitation
            {
                'title': 'Sports Rehabilitation',
                'slug': 'sports-rehabilitation',
                'destination': 'USA',
                'hero_headline': 'Sports Rehabilitation & Performance',
                'hero_subheadline': 'Get back in the game faster with sport-specific recovery protocols.',
                'body': '<p>Whether you\'re a professional athlete or a weekend warrior, our <strong>Sports Rehabilitation</strong> program is designed to get you back to peak performance safely and efficiently.</p><h3>What We Cover</h3><ul><li>ACL & ligament tears</li><li>Ankle sprains & instability</li><li>Muscle strains & tendinopathies</li><li>Achilles tendon injuries</li><li>Sports hernia (athletic pubalgia)</li></ul><h3>Our Sports Rehab Approach</h3><p>We use progressive loading, sport-specific agility drills, plyometric training, and biomechanical analysis to ensure you return to sport stronger than before.</p>',
                'stat_1_label': 'Athletes Treated', 'stat_1_value': '400+',
                'stat_2_label': 'Return Rate', 'stat_2_value': '95%',
                'stat_3_label': 'Sports Covered', 'stat_3_value': '20+',
            },
            {
                'title': 'Athletic Performance',
                'slug': 'athletic-performance',
                'destination': 'USA',
                'hero_headline': 'Athletic Performance Enhancement',
                'hero_subheadline': 'Injury prevention and performance optimization for athletes at all levels.',
                'body': '<p>Preventing injuries before they happen is the hallmark of elite sports medicine. Our <strong>Athletic Performance</strong> program combines functional movement screening, strength assessments, and personalized conditioning.</p><h3>Services</h3><ul><li>Functional Movement Screen (FMS)</li><li>Biomechanical running analysis</li><li>Prehab programs for injury prevention</li><li>Return-to-sport testing protocols</li></ul>',
                'stat_1_label': 'Athletes Screened', 'stat_1_value': '250+',
                'stat_2_label': 'Injury Reduction', 'stat_2_value': '60%',
                'stat_3_label': 'Programs', 'stat_3_value': 'Custom',
            },
            # AUS → Neurological & Stroke Recovery
            {
                'title': 'Stroke Rehabilitation',
                'slug': 'stroke-rehabilitation',
                'destination': 'AUS',
                'hero_headline': 'Neurological & Stroke Rehabilitation',
                'hero_subheadline': 'Specialized neuro-physiotherapy to restore mobility and independence after stroke.',
                'body': '<p>A stroke can fundamentally alter a person\'s ability to move, balance, and perform daily tasks. Our <strong>Neurological Rehabilitation</strong> program harnesses neuroplasticity through intensive, repetitive, task-specific training.</p><h3>Focus Areas</h3><ul><li>Gait and walking retraining</li><li>Balance and fall prevention</li><li>Constraint-Induced Movement Therapy (CIMT)</li><li>Upper limb functional recovery</li><li>Home-based stroke care visits</li></ul>',
                'stat_1_label': 'Patients Served', 'stat_1_value': '200+',
                'stat_2_label': 'Mobility Gain', 'stat_2_value': '85%',
                'stat_3_label': 'Home Visits', 'stat_3_value': 'Available',
            },
            {
                'title': 'Balance & Falls Prevention',
                'slug': 'balance-falls-prevention',
                'destination': 'AUS',
                'hero_headline': 'Balance & Falls Prevention Program',
                'hero_subheadline': 'Reduce your risk of falling and improve confidence in daily movement.',
                'body': '<p>Falls are a leading cause of injury, especially for older adults and those recovering from neurological conditions. Our <strong>Balance & Falls Prevention</strong> program uses evidence-based exercises to improve stability, coordination, and confidence.</p><h3>What\'s Included</h3><ul><li>Comprehensive balance assessment</li><li>Vestibular rehabilitation</li><li>Strength and coordination training</li><li>Home safety evaluation</li></ul>',
                'stat_1_label': 'Fall Reduction', 'stat_1_value': '70%',
                'stat_2_label': 'Patients', 'stat_2_value': '150+',
                'stat_3_label': 'Assessment', 'stat_3_value': 'Free',
            },
            # ALL → General Wellness & Prevention
            {
                'title': 'General Wellness',
                'slug': 'general-wellness',
                'destination': 'ALL',
                'hero_headline': 'General Wellness & Prevention',
                'hero_subheadline': 'Proactive physiotherapy for posture, ergonomics, and overall body wellness.',
                'body': '<p>You don\'t need to be in pain to benefit from physiotherapy. Our <strong>General Wellness</strong> services focus on preventing injuries, improving posture, and keeping you active and pain-free.</p><h3>Our Wellness Services</h3><ul><li>Ergonomic workplace assessments</li><li>Posture correction programs</li><li>Flexibility and mobility training</li><li>Stress-related tension management</li></ul>',
                'stat_1_label': 'Clients Served', 'stat_1_value': '500+',
                'stat_2_label': 'Prevention Rate', 'stat_2_value': '90%',
                'stat_3_label': 'Consultation', 'stat_3_value': 'Free First',
            },
            {
                'title': 'Home Visit Physiotherapy',
                'slug': 'home-visit-physiotherapy',
                'destination': 'ALL',
                'hero_headline': 'Home Visit Physiotherapy',
                'hero_subheadline': 'Professional physiotherapy delivered to your doorstep across Nairobi and surrounding areas.',
                'body': '<p>For patients who cannot easily travel to a clinic — whether recovering from surgery, stroke, or managing chronic conditions — our <strong>Home Visit Physiotherapy</strong> service brings expert care directly to your home.</p><h3>What We Provide</h3><ul><li>Full assessment and treatment at home</li><li>Post-surgical rehabilitation visits</li><li>Stroke and neurological rehab at home</li><li>Elderly care and mobility programs</li></ul>',
                'stat_1_label': 'Home Visits/Month', 'stat_1_value': '60+',
                'stat_2_label': 'Areas Covered', 'stat_2_value': 'Nairobi+',
                'stat_3_label': 'Booking', 'stat_3_value': 'Same Day',
            },
            {
                'title': 'Dry Needling Therapy',
                'slug': 'dry-needling-therapy',
                'destination': 'ALL',
                'hero_headline': 'Dry Needling & Trigger Point Therapy',
                'hero_subheadline': 'Targeted relief for muscle knots, tension, and chronic myofascial pain.',
                'body': '<p><strong>Dry needling</strong> involves inserting thin, sterile needles into myofascial trigger points (muscle knots) to release tension, improve blood flow, and reduce pain. It is a powerful adjunct to traditional physiotherapy.</p><h3>Conditions Treated</h3><ul><li>Chronic neck and shoulder tension</li><li>Lower back muscle spasm</li><li>Tennis and golfer\'s elbow</li><li>Headaches caused by muscle tension</li><li>Plantar fasciitis</li></ul>',
                'stat_1_label': 'Pain Reduction', 'stat_1_value': '80%',
                'stat_2_label': 'Sessions Needed', 'stat_2_value': '3-6',
                'stat_3_label': 'Duration', 'stat_3_value': '30-45 min',
            },
        ]

        for page_data in pages_data:
            page, created = LocalPage.objects.update_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(f"  {status}: {page.title}")

    def _update_destination_links(self):
        """Point destination cards to their filtered destination pages."""
        dest_url_map = {
            'Orthopedic & Spine Care': '/destinations/uk/',
            'Sports Rehabilitation': '/destinations/usa/',
            'Neurological & Stroke Recovery': '/destinations/aus/',
        }
        for dest in DestinationHighlight.objects.all():
            url = dest_url_map.get(dest.country_name, '#')
            if dest.link_url != url:
                dest.link_url = url
                dest.save()
                self.stdout.write(f"  Updated: {dest.country_name} -> {url}")

    def _update_pathway_links(self):
        """Point pathway highlights to their actual LocalPage URLs."""
        slug_map = {
            'Back Pain Clinic': 'back-pain-clinic',
            'Post-Surgical Rehabilitation': 'post-surgical-rehab',
            'Stroke Rehabilitation': 'stroke-rehabilitation',
            'General Wellness': 'general-wellness',
            'Home Visit Physiotherapy': 'home-visit-physiotherapy',
            'Dry Needling Therapy': 'dry-needling-therapy',
            'Athletic Performance': 'athletic-performance',
        }
        for pw in PathwayHighlight.objects.all():
            slug = slug_map.get(pw.title)
            if slug:
                url = f'/destinations/page/{slug}/'
                if pw.link_url != url:
                    pw.link_url = url
                    pw.save()
                    self.stdout.write(f"  Updated: {pw.title} -> {url}")

    def _update_footer_links(self):
        """Replace all '#' footer links with real URLs."""
        # Delete and recreate all footer data to ensure consistency
        FooterLink.objects.all().delete()
        FooterLinkCategory.objects.all().delete()

        categories_data = [
            {'name': 'Explore', 'order': 1},
            {'name': 'Specialties', 'order': 2},
            {'name': 'Resources', 'order': 3},
            {'name': 'Contact', 'order': 4},
        ]

        categories = {}
        for cat_data in categories_data:
            cat = FooterLinkCategory.objects.create(**cat_data)
            categories[cat.name] = cat

        links_data = [
            # Explore - using named URLs (resolved by get_url property)
            {'category': categories['Explore'], 'title': 'Home', 'url': 'home', 'order': 1},
            {'category': categories['Explore'], 'title': 'Journal', 'url': 'seo:blog_list', 'order': 2},
            {'category': categories['Explore'], 'title': 'FAQ', 'url': 'seo:faq_list', 'order': 3},
            {'category': categories['Explore'], 'title': 'All Services', 'url': 'seo:local_page_list', 'order': 4},

            # Specialties - direct URLs to LocalPages
            {'category': categories['Specialties'], 'title': 'Orthopedic Care', 'url': '/destinations/page/orthopedic-care/', 'order': 1},
            {'category': categories['Specialties'], 'title': 'Sports Rehabilitation', 'url': '/destinations/page/sports-rehabilitation/', 'order': 2},
            {'category': categories['Specialties'], 'title': 'Stroke Rehabilitation', 'url': '/destinations/page/stroke-rehabilitation/', 'order': 3},
            {'category': categories['Specialties'], 'title': 'Home Visit Physio', 'url': '/destinations/page/home-visit-physiotherapy/', 'order': 4},

            # Resources - direct URLs to blog posts and LocalPages
            {'category': categories['Resources'], 'title': 'Back Pain Guide', 'url': '/destinations/page/back-pain-clinic/', 'order': 1},
            {'category': categories['Resources'], 'title': 'Ergonomic Tips', 'url': '/destinations/page/general-wellness/', 'order': 2},
            {'category': categories['Resources'], 'title': 'Post-Surgery Rehab', 'url': '/destinations/page/post-surgical-rehab/', 'order': 3},
            {'category': categories['Resources'], 'title': 'Dry Needling', 'url': '/destinations/page/dry-needling-therapy/', 'order': 4},

            # Contact - real links
            {'category': categories['Contact'], 'title': 'WhatsApp Us', 'url': 'https://wa.me/254700537371', 'order': 1},
            {'category': categories['Contact'], 'title': 'FAQ', 'url': 'seo:faq_list', 'order': 2},
            {'category': categories['Contact'], 'title': 'Book a Session', 'url': 'account_signup', 'order': 3},
            {'category': categories['Contact'], 'title': 'Login', 'url': 'account_login', 'order': 4},
        ]

        for link_data in links_data:
            FooterLink.objects.create(**link_data)

        self.stdout.write(f"  Created {len(links_data)} footer links across {len(categories_data)} categories")
