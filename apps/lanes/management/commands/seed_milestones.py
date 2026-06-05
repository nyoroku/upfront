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
        milestones = [
            # ── UK Pathway ──
            {'destination': 'UK', 'order': 1, 'title': 'English Language Test',
             'slug': 'uk-english-test', 'icon_name': 'language',
             'description': 'Pass your IELTS Academic (7.0 overall) or OET (Grade B). This is the first requirement for NMC registration. We provide practice tests and study materials to help you prepare.',
             'is_free': True, 'required_docs': ['ielts_certificate']},
            {'destination': 'UK', 'order': 2, 'title': 'CBT Exam Preparation',
             'slug': 'uk-cbt-prep', 'icon_name': 'academic-cap',
             'description': 'Prepare for and pass the NMC Computer-Based Test. Covers numeracy and clinical nursing knowledge. Access 500+ practice questions and timed mock exams.',
             'is_free': False, 'required_docs': ['cbt_result']},
            {'destination': 'UK', 'order': 3, 'title': 'Document Verification',
             'slug': 'uk-doc-verification', 'icon_name': 'document-check',
             'description': 'Upload and verify your nursing qualifications, NCK registration, and other supporting documents. Our team reviews each document within 48 hours.',
             'is_free': False, 'required_docs': ['nursing_degree', 'nck_certificate', 'good_conduct']},
            {'destination': 'UK', 'order': 4, 'title': 'NMC Registration',
             'slug': 'uk-nmc-registration', 'icon_name': 'identification',
             'description': 'Apply for NMC registration using your verified documents and exam results. We guide you through the online application process step by step.',
             'is_free': False, 'required_docs': ['nmc_application_receipt']},
            {'destination': 'UK', 'order': 5, 'title': 'OSCE Preparation',
             'slug': 'uk-osce-prep', 'icon_name': 'clipboard-document-check',
             'description': 'Prepare for the Objective Structured Clinical Examination. Practice clinical scenarios, communication skills, and practical nursing procedures.',
             'is_free': False, 'required_docs': ['osce_result']},
            {'destination': 'UK', 'order': 6, 'title': 'Job Placement',
             'slug': 'uk-job-placement', 'icon_name': 'briefcase',
             'description': 'Access NHS job listings matched to your profile and preferences. We connect you with NHS Trusts actively recruiting international nurses in London, Manchester, and beyond.',
             'is_free': False, 'required_docs': ['cv', 'reference_letters']},
            {'destination': 'UK', 'order': 7, 'title': 'Visa & Relocation',
             'slug': 'uk-visa-relocation', 'icon_name': 'globe-alt',
             'description': 'Apply for the Health and Care Worker Visa with your Certificate of Sponsorship. We help with visa applications, flight booking, and initial accommodation.',
             'is_free': False, 'required_docs': ['visa_approval', 'flight_itinerary']},

            # ── USA Pathway ──
            {'destination': 'USA', 'order': 1, 'title': 'English Language Test',
             'slug': 'usa-english-test', 'icon_name': 'language',
             'description': 'Pass IELTS Academic (6.5+) or TOEFL iBT (83+). Required for CGFNS VisaScreen certification. Our preparation course focuses on healthcare-specific English.',
             'is_free': True, 'required_docs': ['ielts_certificate']},
            {'destination': 'USA', 'order': 2, 'title': 'NCLEX-RN Preparation',
             'slug': 'usa-nclex-prep', 'icon_name': 'academic-cap',
             'description': 'Prepare for the NCLEX-RN exam with 3,000+ practice questions, adaptive learning, and detailed explanations. Pass on your first attempt with our proven study method.',
             'is_free': False, 'required_docs': ['nclex_result']},
            {'destination': 'USA', 'order': 3, 'title': 'Credential Evaluation',
             'slug': 'usa-credential-eval', 'icon_name': 'document-check',
             'description': 'Submit your nursing credentials to CGFNS for evaluation. We guide you through the process and help with document apostille and notarization.',
             'is_free': False, 'required_docs': ['cgfns_evaluation', 'nursing_degree']},
            {'destination': 'USA', 'order': 4, 'title': 'VisaScreen Certificate',
             'slug': 'usa-visascreen', 'icon_name': 'shield-check',
             'description': 'Obtain your VisaScreen certificate from CGFNS, verifying your education, licensure, and English proficiency. Required for all US work visa applications.',
             'is_free': False, 'required_docs': ['visascreen_certificate']},
            {'destination': 'USA', 'order': 5, 'title': 'State Licensure',
             'slug': 'usa-state-licensure', 'icon_name': 'identification',
             'description': 'Apply for nursing licensure in your target state. Requirements vary by state. We help you choose the best state and navigate the application process.',
             'is_free': False, 'required_docs': ['state_license']},
            {'destination': 'USA', 'order': 6, 'title': 'Job & Visa Processing',
             'slug': 'usa-job-visa', 'icon_name': 'globe-alt',
             'description': 'Match with US healthcare employers, receive a job offer, and begin EB-3 Green Card or H-1B visa processing. We manage the full immigration timeline.',
             'is_free': False, 'required_docs': ['job_offer', 'visa_approval']},

            # ── Australia Pathway ──
            {'destination': 'AU', 'order': 1, 'title': 'English Language Test',
             'slug': 'au-english-test', 'icon_name': 'language',
             'description': 'Achieve IELTS 7.0 in each band or OET Grade B. Australia has strict English requirements. Our course focuses on the specific areas nurses find most challenging.',
             'is_free': True, 'required_docs': ['ielts_certificate']},
            {'destination': 'AU', 'order': 2, 'title': 'ANMAC Skills Assessment',
             'slug': 'au-anmac-assessment', 'icon_name': 'clipboard-document-check',
             'description': 'Submit your nursing qualifications to ANMAC for a skills assessment. You need at least 450 hours of clinical practice in the past 5 years.',
             'is_free': False, 'required_docs': ['anmac_assessment', 'nursing_degree']},
            {'destination': 'AU', 'order': 3, 'title': 'Document Verification',
             'slug': 'au-doc-verification', 'icon_name': 'document-check',
             'description': 'Upload and verify all supporting documents including your nursing degree, clinical hours log, character references, and police clearance.',
             'is_free': False, 'required_docs': ['nursing_degree', 'clinical_hours', 'police_clearance']},
            {'destination': 'AU', 'order': 4, 'title': 'AHPRA Registration',
             'slug': 'au-ahpra-registration', 'icon_name': 'identification',
             'description': 'Apply for registration with the Australian Health Practitioner Regulation Agency. We walk you through the online portal and ensure all requirements are met.',
             'is_free': False, 'required_docs': ['ahpra_registration']},
            {'destination': 'AU', 'order': 5, 'title': 'Job & Visa Processing',
             'slug': 'au-job-visa', 'icon_name': 'globe-alt',
             'description': 'Connect with Australian healthcare employers and apply for a Skilled Worker Visa (subclass 482 or 494). We manage employer sponsorship and visa timelines.',
             'is_free': False, 'required_docs': ['job_offer', 'visa_approval']},
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
