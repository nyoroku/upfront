import os
from django.core.management.base import BaseCommand
from apps.seo.models import FAQCategory, FAQ

class Command(BaseCommand):
    help = 'Seeds the database with Upfront Physiotherapy FAQs.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Physiotherapy FAQs...')

        FAQ.objects.all().delete()
        FAQCategory.objects.all().delete()

        categories_data = [
            {
                'name': 'General Physiotherapy',
                'slug': 'general-physio',
                'order': 1,
                'meta_title': 'General Physiotherapy FAQs — Upfront',
                'meta_description': 'Frequently asked questions about physical therapy, what to expect, and self-referral guidelines.'
            },
            {
                'name': 'Treatments & Specialties',
                'slug': 'treatments-specialties',
                'order': 2,
                'meta_title': 'Physiotherapy Treatments FAQs — Upfront',
                'meta_description': 'FAQs on sports injury rehab, orthopedic spine care, stroke rehab, dry needling, and home visits.'
            },
            {
                'name': 'Appointments & Booking',
                'slug': 'appointments-booking',
                'order': 3,
                'meta_title': 'Appointments & Insurance FAQs — Upfront',
                'meta_description': 'Details on session durations, accepted insurance policies, and booking info.'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            cat = FAQCategory.objects.create(**cat_data)
            categories[cat.slug] = cat

        faqs_data = [
            # General Physiotherapy
            {
                'question': 'What is physiotherapy and how can it help me?',
                'answer': '<p>Physiotherapy is a evidence-based healthcare profession focused on restoring movement, strength, and function when someone is affected by injury, illness, or disability. Through tailored exercises, manual therapy, education, and expert advice, certified physical therapist Dan Mwangi Gichobi helps you manage pain, recover from physical trauma, and enhance athletic performance.</p>',
                'category': categories['general-physio'],
                'order': 1,
            },
            {
                'question': "Do I need a doctor's referral to see a physiotherapist?",
                'answer': '<p>No, in Kenya, you do not need a doctor\'s referral to see a certified physiotherapist. You can book an appointment directly with Upfront for assessment and treatment. However, if you are planning to claim from insurance, some insurance providers may require a referral from a general practitioner or specialist.</p>',
                'category': categories['general-physio'],
                'order': 2,
            },
            {
                'question': 'What should I wear to my physiotherapy sessions?',
                'answer': '<p>We recommend wearing comfortable, loose-fitting clothing that allows easy access to the area being treated and doesn\'t restrict your movement. For example, shorts for knee/hip issues, or a tank top/t-shirt for neck/shoulder issues, along with stable athletic shoes.</p>',
                'category': categories['general-physio'],
                'order': 3,
            },
            
            # Treatments & Specialties
            {
                'question': 'What conditions do you treat at Upfront?',
                'answer': '<p>We treat a wide range of orthopedic, sports, neurological, and pediatric conditions. This includes chronic back and neck pain, sports injuries (sprains, strains, ligament tears), post-operative recovery (joint replacements, post-fracture stiffness), stroke rehabilitation, and pediatric developmental delays.</p>',
                'category': categories['treatments-specialties'],
                'order': 4,
            },
            {
                'question': 'What is dry needling and is it safe?',
                'answer': '<p>Dry needling is a highly effective treatment technique using thin, sterile monofilament needles to target myofascial trigger points (muscle knots) to relieve pain and improve range of motion. It is extremely safe and well-tolerated when performed by a certified professional like Dan Mwangi Gichobi.</p>',
                'category': categories['treatments-specialties'],
                'order': 5,
            },
            {
                'question': 'Do you offer home-based physiotherapy services?',
                'answer': '<p>Yes, we offer home-based physiotherapy visits in Nairobi and surrounding areas for patients with limited mobility, stroke survivors undergoing neurological rehab, or those who prefer the comfort and convenience of therapy at home.</p>',
                'category': categories['treatments-specialties'],
                'order': 6,
            },

            # Appointments & Booking
            {
                'question': 'How long does a typical physiotherapy session last?',
                'answer': '<p>An initial assessment session typically lasts 45 to 60 minutes, which includes a comprehensive physical evaluation, diagnosis, and initial treatment. Follow-up sessions usually last between 30 to 45 minutes depending on your custom treatment plan.</p>',
                'category': categories['appointments-booking'],
                'order': 7,
            },
            {
                'question': 'Does Upfront accept health insurance?',
                'answer': '<p>Yes, we accept major health insurance providers in Kenya for outpatient physiotherapy services. Please contact our team prior to your session to confirm whether your specific insurance cover is accepted and if pre-authorization is required.</p>',
                'category': categories['appointments-booking'],
                'order': 8,
            },
            {
                'question': 'How many sessions will I need to recover?',
                'answer': '<p>The number of sessions depends entirely on your diagnosis, the severity of your condition, and how your body responds to therapy. After your initial assessment, we will outline a personalized recovery plan with an estimated timeline of sessions required.</p>',
                'category': categories['appointments-booking'],
                'order': 9,
            },
        ]

        for faq_data in faqs_data:
            FAQ.objects.create(**faq_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(categories_data)} FAQ categories and {len(faqs_data)} FAQs.'))
