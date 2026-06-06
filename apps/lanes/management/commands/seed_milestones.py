"""
Seeds MilestoneTemplates for all destinations.
Run: python manage.py seed_milestones
"""
from django.core.management.base import BaseCommand
from apps.lanes.models import MilestoneTemplate


class Command(BaseCommand):
    help = 'Seeds milestone templates for UK, USA, and AU pathways'

    def handle(self, *args, **kwargs):
        self.stdout.write("=== Seeding Milestone Templates ===")
        # Clean existing milestone templates
        MilestoneTemplate.objects.all().delete()
        milestones = [
            # ── Orthopedic & Spine Care (UK) ──
            {'destination': 'UK', 'order': 1, 'title': 'Initial Physical Assessment',
             'slug': 'ortho-initial-assessment', 'icon_name': 'identification',
             'description': 'Book and complete your initial physical examination with Dan Mwangi Gichobi to assess joint range of motion, muscle strength, and establish a clinical diagnosis.',
             'is_free': True, 'required_docs': ['identity_document']},
            {'destination': 'UK', 'order': 2, 'title': 'Clinical Diagnostic Review',
             'slug': 'ortho-diagnostic-review', 'icon_name': 'document-check',
             'description': 'Review of medical imaging reports (X-rays, MRIs) and orthopedic clinical records to refine our clinical rehabilitation strategy.',
             'is_free': False, 'required_docs': ['medical_imaging_report']},
            {'destination': 'UK', 'order': 3, 'title': 'Active Rehabilitation Phase',
             'slug': 'ortho-active-rehab', 'icon_name': 'academic-cap',
             'description': 'Undergo custom clinical sessions consisting of joint mobilizations, spinal alignments, myofascial release, and progressive loading.',
             'is_free': False, 'required_docs': ['rehab_attendance_log']},
            {'destination': 'UK', 'order': 4, 'title': 'Progress & Range of Motion Evaluation',
             'slug': 'ortho-progress-review', 'icon_name': 'clipboard-document-check',
             'description': 'Perform intermediate clinical tests to measure objective improvements in pain levels, range of motion, and muscular strength.',
             'is_free': False, 'required_docs': ['progress_report']},
            {'destination': 'UK', 'order': 5, 'title': 'Home Exercise & Maintenance Setup',
             'slug': 'ortho-home-setup', 'icon_name': 'globe-alt',
             'description': 'Establish a structured home exercise plan to maintain clinical gains, build posture awareness, and prevent future re-injury.',
             'is_free': False, 'required_docs': ['home_exercise_log']},
            {'destination': 'UK', 'order': 6, 'title': 'Final Discharge Assessment',
             'slug': 'ortho-final-discharge', 'icon_name': 'shield-check',
             'description': 'Undergo final testing to verify treatment goals have been met. Receive your long-term wellness guides and discharge summary.',
             'is_free': False, 'required_docs': ['discharge_summary']},

            # ── Sports & Active Rehab (USA) ──
            {'destination': 'USA', 'order': 1, 'title': 'Sports Injury Assessment',
             'slug': 'sports-initial-assessment', 'icon_name': 'identification',
             'description': 'Undergo a comprehensive sports-specific injury evaluation and functional movement screen (FMS) to identify biomechanical imbalances.',
             'is_free': True, 'required_docs': ['identity_document']},
            {'destination': 'USA', 'order': 2, 'title': 'Athletic Movement Analysis',
             'slug': 'sports-movement-analysis', 'icon_name': 'document-check',
             'description': 'Analyze specific athletic demands, muscle activation deficits, and load capacity requirements to customize your return-to-sport path.',
             'is_free': False, 'required_docs': ['clinical_referral']},
            {'destination': 'USA', 'order': 3, 'title': 'Progressive Loading & Conditioning',
             'slug': 'sports-loading-rehab', 'icon_name': 'academic-cap',
             'description': 'Rebuild tissue tolerance, eccentric muscle strength, and joint stability under sports-simulated loads and specialized dry needling.',
             'is_free': False, 'required_docs': ['loading_progression_log']},
            {'destination': 'USA', 'order': 4, 'title': 'Sports Agility & Plyometric Re-entry',
             'slug': 'sports-agility-plyo', 'icon_name': 'clipboard-document-check',
             'description': 'Reintroduce dynamic movements like running, cutting, jumping, and landing mechanics to prepare your body for full training intensity.',
             'is_free': False, 'required_docs': ['agility_evaluation_sheet']},
            {'destination': 'USA', 'order': 5, 'title': 'Return-to-Sport Testing Battery',
             'slug': 'sports-return-testing', 'icon_name': 'globe-alt',
             'description': 'Pass a strict physical and psychological readiness assessment to ensure you are fully prepared and safe to return to competitive play.',
             'is_free': False, 'required_docs': ['readiness_scorecard']},
            {'destination': 'USA', 'order': 6, 'title': 'Discharge & Performance Integration',
             'slug': 'sports-discharge', 'icon_name': 'shield-check',
             'description': 'Receive clearance for sports entry alongside an injury prevention (prehab) protocol and conditioning plan for peak athletic performance.',
             'is_free': False, 'required_docs': ['discharge_certificate']},

            # ── Stroke & Neuro Care (AU) ──
            {'destination': 'AU', 'order': 1, 'title': 'Neurological Assessment',
             'slug': 'neuro-initial-assessment', 'icon_name': 'identification',
             'description': 'Complete a detailed neurological evaluation focusing on motor patterns, sensory pathway integrity, coordination, and balance control.',
             'is_free': True, 'required_docs': ['identity_document']},
            {'destination': 'AU', 'order': 2, 'title': 'Goal Mapping & Care Coordination',
             'slug': 'neuro-goal-mapping', 'icon_name': 'document-check',
             'description': 'Establish personal independence goals, define target activities of daily living (ADLs), and coordinate with your physician.',
             'is_free': False, 'required_docs': ['physician_clearance']},
            {'destination': 'AU', 'order': 3, 'title': 'Neuroplasticity & Task Training',
             'slug': 'neuro-active-rehab', 'icon_name': 'academic-cap',
             'description': 'Undergo intensive task-oriented movement re-education and active-assisted exercises to stimulate new neural pathways.',
             'is_free': False, 'required_docs': ['session_attendance_log']},
            {'destination': 'AU', 'order': 4, 'title': 'Gait & Balance Restoration',
             'slug': 'neuro-gait-balance', 'icon_name': 'clipboard-document-check',
             'description': 'Focus on safety, retraining walking mechanics, posture, fall-prevention reflexes, and walking aid optimization.',
             'is_free': False, 'required_docs': ['balance_scorecard']},
            {'destination': 'AU', 'order': 5, 'title': 'Home Safety & Caregiver Coaching',
             'slug': 'neuro-caregiver-coaching', 'icon_name': 'globe-alt',
             'description': 'Conduct a home safety check and train caregivers on assisted transfers, safe positioning, and daily home movement logs.',
             'is_free': False, 'required_docs': ['home_safety_checklist']},
            {'destination': 'AU', 'order': 6, 'title': 'Final Independence Evaluation',
             'slug': 'neuro-final-discharge', 'icon_name': 'shield-check',
             'description': 'Review functional milestones. Receive a long-term home wellness program and discharge summary indicating level of functional independence.',
             'is_free': False, 'required_docs': ['discharge_summary']},
        ]

        prev_by_dest = {}
        for m_data in milestones:
            dest = m_data['destination']
            unlock_after = prev_by_dest.get(dest)
            obj, created = MilestoneTemplate.objects.update_or_create(
                slug=m_data['slug'],
                defaults={**m_data, 'unlock_after': unlock_after}
            )
            prev_by_dest[dest] = obj
            st = 'Created' if created else 'Updated'
            self.stdout.write(f"  {st}: [{dest}] {m_data['order']}. {m_data['title']}")

        self.stdout.write(self.style.SUCCESS(
            f"Done! {MilestoneTemplate.objects.count()} milestone templates in database."
        ))
