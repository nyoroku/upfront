"""
Seeds courses with modules and quizzes.
Run: python manage.py seed_courses
"""
from django.core.management.base import BaseCommand
from apps.courses.models import Course, Module, Quiz, Question, Choice
from apps.lanes.models import MilestoneTemplate


class Command(BaseCommand):
    help = 'Seeds courses with modules, quizzes, and questions'

    def handle(self, *args, **kwargs):
        self.stdout.write("=== Seeding Courses ===")

        courses_data = [
            # ── CBT Preparation (UK) ──
            {
                'title': 'CBT Exam Mastery',
                'slug': 'cbt-exam-mastery',
                'exam_type': 'CBT',
                'destination': 'UK',
                'description': '<p>Complete preparation for the NMC Computer-Based Test. Covers Part A (Numeracy) and Part B (Clinical Nursing) with hundreds of practice questions and detailed explanations.</p><p>This course is designed for Kenyan nurses preparing for UK registration.</p>',
                'is_free': False,
                'milestone_slug': 'uk-cbt-prep',
                'modules': [
                    {'order': 1, 'title': 'Introduction to the CBT', 'duration_minutes': 20, 'is_preview': True},
                    {'order': 2, 'title': 'Drug Dosage Calculations', 'duration_minutes': 45, 'is_preview': False},
                    {'order': 3, 'title': 'Unit Conversions & Infusion Rates', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 4, 'title': 'Patient Safety & Safeguarding', 'duration_minutes': 35, 'is_preview': False},
                    {'order': 5, 'title': 'Infection Control & Prevention', 'duration_minutes': 30, 'is_preview': False},
                    {'order': 6, 'title': 'Medication Administration', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 7, 'title': 'Clinical Decision Making', 'duration_minutes': 35, 'is_preview': False},
                    {'order': 8, 'title': 'Leadership & Management', 'duration_minutes': 30, 'is_preview': False},
                ],
                'quiz': {
                    'title': 'CBT Mock Exam — Part B',
                    'time_limit_minutes': 90,
                    'pass_mark_percent': 60,
                    'questions': [
                        {'body': 'A patient is prescribed 500mg of amoxicillin. The tablets available are 250mg each. How many tablets should the nurse administer?',
                         'explanation': 'Dose required / Dose available = 500mg / 250mg = 2 tablets.',
                         'choices': [('1 tablet', False), ('2 tablets', True), ('3 tablets', False), ('4 tablets', False)]},
                        {'body': 'What is the primary purpose of hand hygiene in healthcare settings?',
                         'explanation': 'Hand hygiene is the single most important measure to prevent healthcare-associated infections (HCAIs).',
                         'choices': [('To keep hands moisturised', False), ('To prevent healthcare-associated infections', True), ('To comply with hospital dress code', False), ('To remove visible dirt only', False)]},
                        {'body': 'A nurse discovers a medication error. What should be the FIRST action?',
                         'explanation': 'Patient safety is the priority. Assess the patient first, then report through proper channels.',
                         'choices': [('File an incident report', False), ('Inform the pharmacy', False), ('Assess the patient for any adverse effects', True), ('Contact the prescribing doctor', False)]},
                        {'body': 'When administering an intramuscular injection to an adult, which site is recommended for volumes greater than 2ml?',
                         'explanation': 'The vastus lateralis and ventrogluteal sites can accommodate larger volumes (up to 5ml) compared to the deltoid (max 1ml).',
                         'choices': [('Deltoid', False), ('Dorsogluteal', False), ('Ventrogluteal', True), ('Subcutaneous tissue', False)]},
                        {'body': 'A patient has a NEWS2 score of 7. What level of clinical response is required?',
                         'explanation': 'A NEWS2 score of 7 or more triggers an emergency response. The nurse should escalate immediately.',
                         'choices': [('Routine monitoring every 12 hours', False), ('Increase monitoring to every 4 hours', False), ('Urgent clinical review within 1 hour', False), ('Emergency response — immediate clinical review', True)]},
                    ]
                }
            },

            # ── IELTS for Nurses (ALL) ──
            {
                'title': 'IELTS Academic for Nurses',
                'slug': 'ielts-academic-nurses',
                'exam_type': 'IELTS',
                'destination': 'UK',
                'description': '<p>Targeted IELTS preparation for healthcare professionals. Focus on medical vocabulary, clinical report writing, and healthcare-focused speaking topics.</p><p>Aim for Band 7.0+ with our structured 8-week programme.</p>',
                'is_free': True,
                'milestone_slug': 'uk-english-test',
                'modules': [
                    {'order': 1, 'title': 'Understanding the IELTS Format', 'duration_minutes': 25, 'is_preview': True},
                    {'order': 2, 'title': 'Listening — Healthcare Scenarios', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 3, 'title': 'Reading — Medical Journal Passages', 'duration_minutes': 45, 'is_preview': False},
                    {'order': 4, 'title': 'Writing Task 1 — Graphs & Charts', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 5, 'title': 'Writing Task 2 — Healthcare Essays', 'duration_minutes': 45, 'is_preview': False},
                    {'order': 6, 'title': 'Speaking — Clinical Communication', 'duration_minutes': 35, 'is_preview': False},
                ],
                'quiz': {
                    'title': 'IELTS Reading Practice Test',
                    'time_limit_minutes': 60,
                    'pass_mark_percent': 70,
                    'questions': [
                        {'body': 'In IELTS Academic WritingTask 1, what is the recommended word count?',
                         'explanation': 'Task 1 requires at least 150 words. Going significantly under will result in a penalty.',
                         'choices': [('100 words', False), ('150 words', True), ('200 words', False), ('250 words', False)]},
                        {'body': 'Which section of IELTS has the strictest time pressure for most test-takers?',
                         'explanation': 'Reading is commonly cited as the most time-pressured section with 40 questions in 60 minutes across 3 passages.',
                         'choices': [('Listening', False), ('Reading', True), ('Writing', False), ('Speaking', False)]},
                        {'body': 'What band score does NMC require for each IELTS component?',
                         'explanation': 'NMC requires minimum 7.0 in Reading, Listening, and Speaking, and 6.5 in Writing.',
                         'choices': [('6.0 in each', False), ('6.5 in each', False), ('7.0 Reading/Listening/Speaking, 6.5 Writing', True), ('7.5 in each', False)]},
                    ]
                }
            },

            # ── NCLEX-RN Preparation (USA) ──
            {
                'title': 'NCLEX-RN Comprehensive Review',
                'slug': 'nclex-rn-comprehensive',
                'exam_type': 'NCLEX',
                'destination': 'USA',
                'description': '<p>Master the NCLEX-RN with our comprehensive review course. Covers all client needs categories with 3,000+ practice questions.</p><p>Our adaptive learning system focuses on your weak areas for maximum efficiency.</p>',
                'is_free': False,
                'milestone_slug': 'usa-nclex-prep',
                'modules': [
                    {'order': 1, 'title': 'NCLEX Format & Strategies', 'duration_minutes': 30, 'is_preview': True},
                    {'order': 2, 'title': 'Safe & Effective Care Environment', 'duration_minutes': 50, 'is_preview': False},
                    {'order': 3, 'title': 'Health Promotion & Maintenance', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 4, 'title': 'Psychosocial Integrity', 'duration_minutes': 35, 'is_preview': False},
                    {'order': 5, 'title': 'Physiological Integrity — Basic', 'duration_minutes': 50, 'is_preview': False},
                    {'order': 6, 'title': 'Physiological Integrity — Advanced', 'duration_minutes': 50, 'is_preview': False},
                    {'order': 7, 'title': 'Pharmacology & IV Therapy', 'duration_minutes': 45, 'is_preview': False},
                    {'order': 8, 'title': 'Prioritisation & Delegation', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 9, 'title': 'Next Generation NCLEX (NGN)', 'duration_minutes': 35, 'is_preview': False},
                ],
                'quiz': {
                    'title': 'NCLEX-RN Practice Exam',
                    'time_limit_minutes': 120,
                    'pass_mark_percent': 65,
                    'questions': [
                        {'body': 'A nurse is caring for 4 patients. Which patient should be assessed FIRST?',
                         'explanation': 'Using the ABCs framework, the patient with respiratory distress (airway/breathing) takes priority.',
                         'choices': [('Patient with a blood glucose of 180 mg/dL', False), ('Patient complaining of nausea after surgery', False), ('Patient with new onset of dyspnoea and oxygen saturation of 88%', True), ('Patient requesting pain medication rated 6/10', False)]},
                        {'body': 'Which task can be safely delegated to an unlicensed assistive personnel (UAP)?',
                         'explanation': 'UAPs can perform routine, non-invasive tasks like measuring vital signs on stable patients. Assessment, teaching, and medication are RN responsibilities.',
                         'choices': [('Teaching a newly diagnosed diabetic about insulin', False), ('Administering oral medications', False), ('Measuring vital signs on a stable post-operative patient', True), ('Assessing a patient\'s wound for signs of infection', False)]},
                        {'body': 'A patient is on a heparin drip. The aPTT result is 120 seconds (therapeutic range: 60-80 seconds). What should the nurse do?',
                         'explanation': 'An aPTT significantly above therapeutic range indicates over-anticoagulation. Stop the infusion and notify the provider immediately.',
                         'choices': [('Continue the current rate', False), ('Increase the drip rate', False), ('Decrease the drip rate by 50%', False), ('Stop the infusion and notify the healthcare provider', True)]},
                    ]
                }
            },

            # ── Mental Health Nursing (ALL) ──
            {
                'title': 'Mental Health Nursing Essentials',
                'slug': 'mental-health-nursing',
                'exam_type': 'GENERAL',
                'destination': 'UK',
                'description': '<p>Build competence in mental health nursing for international practice. Covers assessment frameworks, therapeutic communication, medication management, and crisis intervention used in UK and US settings.</p>',
                'is_free': False,
                'milestone_slug': None,
                'modules': [
                    {'order': 1, 'title': 'Introduction to Mental Health Nursing', 'duration_minutes': 25, 'is_preview': True},
                    {'order': 2, 'title': 'Mental Health Assessment Frameworks', 'duration_minutes': 35, 'is_preview': False},
                    {'order': 3, 'title': 'Therapeutic Communication', 'duration_minutes': 30, 'is_preview': False},
                    {'order': 4, 'title': 'Psychopharmacology', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 5, 'title': 'Crisis Intervention & De-escalation', 'duration_minutes': 35, 'is_preview': False},
                ],
                'quiz': None,
            },
        ]

        for c_data in courses_data:
            milestone = None
            if c_data.get('milestone_slug'):
                milestone = MilestoneTemplate.objects.filter(slug=c_data['milestone_slug']).first()

            modules_data = c_data.pop('modules')
            quiz_data = c_data.pop('quiz', None)
            c_data.pop('milestone_slug', None)

            course, created = Course.objects.update_or_create(
                slug=c_data['slug'],
                defaults={**c_data, 'milestone': milestone, 'total_modules': len(modules_data)}
            )
            st = 'Created' if created else 'Updated'
            self.stdout.write(f"  {st} course: {course.title}")

            # Create modules
            for mod_data in modules_data:
                Module.objects.update_or_create(
                    course=course, order=mod_data['order'],
                    defaults={**mod_data}
                )

            # Create quiz
            if quiz_data:
                questions = quiz_data.pop('questions')
                quiz_obj, _ = Quiz.objects.update_or_create(
                    module=course.modules.last(),
                    defaults={**quiz_data}
                )
                for i, q_data in enumerate(questions):
                    choices = q_data.pop('choices')
                    question, _ = Question.objects.update_or_create(
                        quiz=quiz_obj, order=i + 1,
                        defaults={'body': q_data['body'], 'explanation': q_data['explanation'], 'question_type': 'MCQ'}
                    )
                    question.choices.all().delete()
                    for text, is_correct in choices:
                        Choice.objects.create(question=question, text=text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS(
            f"Done! {Course.objects.count()} courses, {Module.objects.count()} modules in database."
        ))
