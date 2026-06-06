"""
Seeds courses with modules and quizzes for physiotherapy specialties.
Run: python manage.py seed_courses
"""
from django.core.management.base import BaseCommand
from apps.courses.models import Course, Module, Quiz, Question, Choice
from apps.lanes.models import MilestoneTemplate


class Command(BaseCommand):
    help = 'Seeds courses with modules, quizzes, and questions for Upfront Physiotherapy'

    def handle(self, *args, **kwargs):
        self.stdout.write("=== Seeding Courses ===")

        # Clean existing courses to prevent duplicates/errors
        Course.objects.all().delete()

        courses_data = [
            # ── Spine & Joint Care Mastery (Orthopedic / UK) ──
            {
                'title': 'Spine & Joint Care Mastery',
                'slug': 'spine-joint-mastery',
                'exam_type': 'ORTHO',
                'destination': 'UK',
                'description': '<p>Learn the structure of your spine, core activation, and essential daily exercises to prevent and manage lower back pain. Led by Dan Mwangi Gichobi, certified physiotherapist.</p>',
                'is_free': True,
                'milestone_slug': 'ortho-active-rehab',
                'modules': [
                    {'order': 1, 'title': 'Introduction to Spine Anatomy', 'duration_minutes': 20, 'is_preview': True},
                    {'order': 2, 'title': 'Core Activation & Stability Exercises', 'duration_minutes': 30, 'is_preview': False},
                    {'order': 3, 'title': 'Ergonomics & Desk Posture Corrections', 'duration_minutes': 25, 'is_preview': False},
                    {'order': 4, 'title': 'Safe Lifting Mechanics', 'duration_minutes': 25, 'is_preview': False},
                ],
                'quiz': {
                    'title': 'Spine & Joint Safety Quiz',
                    'time_limit_minutes': 20,
                    'pass_mark_percent': 70,
                    'questions': [
                        {
                            'body': 'Which muscle is considered a primary stabilizer of the lumbar spine?',
                            'explanation': 'The Transversus Abdominis (TVA) acts like a natural corset around your lower back to stabilize the spine during movement.',
                            'choices': [('Rectus Abdominis (Six-Pack)', False), ('Transversus Abdominis', True), ('Gluteus Medius', False), ('Biceps Femoris', False)]
                        },
                        {
                            'body': 'How often is it recommended to stand up and move when working a desk job?',
                            'explanation': 'Standing up and moving every 30 to 45 minutes reduces static muscle fatigue and spinal disc compression.',
                            'choices': [('Every 4 hours', False), ('Every 2 hours', False), ('Every 30 to 45 minutes', True), ('Only during lunch break', False)]
                        },
                        {
                            'body': 'When lifting a heavy object, what is the safest posture?',
                            'explanation': 'To prevent back strain, bend at your knees and hips, keep your spine in a neutral alignment, and lift using your leg muscles.',
                            'choices': [('Bend at the waist with straight legs', False), ('Keep your spine neutral, bend at the knees, and lift with your legs', True), ('Twist your torso while lifting', False), ('Pull the object away from your body', False)]
                        },
                    ]
                }
            },

            # ── Sports Injury & Performance (Sports / USA) ──
            {
                'title': 'Sports Injury & Athletic Recovery',
                'slug': 'sports-injury-recovery',
                'exam_type': 'SPORTS',
                'destination': 'USA',
                'description': '<p>Structured recovery protocols for common athletic injuries such as ligament sprains, muscle strains, and tendon care. Learn progressive loading and safe return-to-sport benchmarks.</p>',
                'is_free': False,
                'milestone_slug': 'sports-loading-rehab',
                'modules': [
                    {'order': 1, 'title': 'Acute Injury Management (PEACE & LOVE)', 'duration_minutes': 25, 'is_preview': True},
                    {'order': 2, 'title': 'Knee & Ankle Stability Drills', 'duration_minutes': 35, 'is_preview': False},
                    {'order': 3, 'title': 'Rotator Cuff & Shoulder Integrity', 'duration_minutes': 30, 'is_preview': False},
                    {'order': 4, 'title': 'Return-to-Sport Functional Assessment', 'duration_minutes': 30, 'is_preview': False},
                ],
                'quiz': {
                    'title': 'Sports Rehabilitation & Recovery Quiz',
                    'time_limit_minutes': 30,
                    'pass_mark_percent': 70,
                    'questions': [
                        {
                            'body': 'In the modern acute injury protocol (PEACE & LOVE), what does the \'A\' in PEACE represent?',
                            'explanation': 'The \'A\' stands for Avoid anti-inflammatory modalities, as natural inflammation is crucial for early tissue healing.',
                            'choices': [('Apply ice immediately', False), ('Avoid anti-inflammatory modalities', True), ('Assess range of motion', False), ('Accelerate activity', False)]
                        },
                        {
                            'body': 'Which muscle group is critical for stability and protecting the ACL in the knee?',
                            'explanation': 'Strengthening the hamstrings helps control anterior shear forces on the tibia, directly supporting and protecting the ACL.',
                            'choices': [('Gastrocnemius', False), ('Quadriceps only', False), ('Hamstrings & Gluteals', True), ('Tibialis Anterior', False)]
                        },
                        {
                            'body': 'When is an athlete considered safe to return to full-contact sports after an injury?',
                            'explanation': 'An athlete must pass a return-to-sport battery testing agility, stability, and achieving symmetrical strength (at least 90%) compared to the uninjured limb.',
                            'choices': [('As soon as visible swelling disappears', False), ('When pain is tolerated with painkillers', False), ('Once they pass functional testing with symmetrical strength', True), ('Exactly 4 weeks after the injury', False)]
                        },
                    ]
                }
            },

            # ── Stroke & Neuro Care (Neuro / AU) ──
            {
                'title': 'Stroke & Neuro Rehab at Home',
                'slug': 'stroke-neuro-home-rehab',
                'exam_type': 'NEURO',
                'destination': 'AU',
                'description': '<p>Step-by-step home-based neurological exercises to promote neuroplasticity, retrain balance and walking mechanics, and establish a safe home care environment.</p>',
                'is_free': False,
                'milestone_slug': 'neuro-active-rehab',
                'modules': [
                    {'order': 1, 'title': 'Introduction to Neuroplasticity & Rehab', 'duration_minutes': 20, 'is_preview': True},
                    {'order': 2, 'title': 'Upper Limb Movement & ROM Drills', 'duration_minutes': 35, 'is_preview': False},
                    {'order': 3, 'title': 'Gait Training & Balance Retention', 'duration_minutes': 40, 'is_preview': False},
                    {'order': 4, 'title': 'Safe Patient Transfers & Caregiver Coaching', 'duration_minutes': 30, 'is_preview': False},
                ],
                'quiz': {
                    'title': 'Neurological Rehab & Caregiver Safety Quiz',
                    'time_limit_minutes': 20,
                    'pass_mark_percent': 70,
                    'questions': [
                        {
                            'body': 'What is neuroplasticity?',
                            'explanation': 'Neuroplasticity is the brain\'s adaptive capability to reorganize and form new neural connections to recover lost functions.',
                            'choices': [('Permanent muscle damage', False), ('The brain\'s ability to reorganize itself by forming new connections', True), ('Hardening of the nervous system', False), ('Loss of brain volume', False)]
                        },
                        {
                            'body': 'Which training concept is most critical for recovering motor control after a stroke?',
                            'explanation': 'Repetitive, high-volume, and task-specific training is key to stimulating neuroplastic changes.',
                            'choices': [('Passive stretching only', False), ('Repetitive, task-specific training', True), ('Resting the limb completely', False), ('Sudden heavy weight lifting', False)]
                        },
                        {
                            'body': 'When assisting a stroke patient with one-sided weakness (hemiplegia) to transfer, what is the best direction?',
                            'explanation': 'For safety and to build confidence, always transfer towards the patient\'s strong (unaffected) side first.',
                            'choices': [('Always transfer towards the weak side', False), ('Always transfer towards the strong (unaffected) side', True), ('It does not matter', False), ('Lift the patient completely without assistance', False)]
                        },
                    ]
                }
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
