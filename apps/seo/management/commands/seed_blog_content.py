"""
Seeds physiotherapy-focused blog posts, updates LocalPage metadata, and adds internal links.
Run with: python manage.py seed_blog_content
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.seo.models import BlogCategory, BlogPost, LocalPage

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds blog posts with internal links and ensures all LocalPages have metadata'

    def handle(self, *args, **kwargs):
        self.stdout.write("=== Seeding Physiotherapy Blog Content ===")
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.first()

        self._create_categories()
        self._create_blog_posts(admin)
        self._update_local_page_metadata()
        self.stdout.write(self.style.SUCCESS("All physiotherapy blog content and metadata seeded successfully!"))

    def _create_categories(self):
        cats = [
            {'name': 'Sports Rehab', 'slug': 'sports-rehab',
             'description': 'Tips and strategies for recovering from sports injuries, sprains, tears, and boosting performance.',
             'meta_title': 'Sports Rehabilitation & Injury Recovery Guides — Upfront',
             'meta_description': 'Expert injury recovery guides, athletic performance tips, and sports rehab articles by Dan Mwangi Gichobi.'},
            {'name': 'Spine & Joint Health', 'slug': 'spine-joint-health',
             'description': 'Guides on back pain, neck pain, joint replacements, and arthritis management.',
             'meta_title': 'Spine & Joint Health Management Guides — Upfront',
             'meta_description': 'Comprehensive guides on lower back pain relief, joint arthroplasty recovery, and neck care.'},
            {'name': 'Neurological Recovery', 'slug': 'neuro-recovery',
             'description': 'Information on stroke rehabilitation, balance disorders, and nerve condition care.',
             'meta_title': 'Neurological Rehabilitation & Stroke Recovery — Upfront',
             'meta_description': 'Articles on stroke recovery, motor function restoration, and neurological physical therapy.'},
            {'name': 'Lifestyle & Ergonomics', 'slug': 'lifestyle-ergonomics',
             'description': 'Practical posture, workplace ergonomics, and injury prevention tips.',
             'meta_title': 'Workspace Ergonomics & Healthy Lifestyle Tips — Upfront',
             'meta_description': 'Posture correction guidelines, occupational ergonomics, and lifestyle adjustments for pain prevention.'},
            {'name': 'Success Stories', 'slug': 'success-stories',
             'description': 'Inspiring real stories of recovery and athletic return from our patients.',
             'meta_title': 'Patient Recovery Success Stories — Upfront',
             'meta_description': 'Real-life recovery success stories from patients who restored their mobility and life with Upfront.'},
        ]
        for cat_data in cats:
            cat, created = BlogCategory.objects.update_or_create(slug=cat_data['slug'], defaults=cat_data)
            st = 'Created' if created else 'Updated'
            self.stdout.write(f"  {st} category: {cat.name}")

    def _create_blog_posts(self, author):
        now = timezone.now()
        posts = [
            # --- Sports Rehab ---
            {
                'title': 'Understanding Sports Hernia: Symptoms, Recovery, and Physical Therapy',
                'slug': 'understanding-sports-hernia-rehab',
                'category_slug': 'sports-rehab',
                'excerpt': 'Learn the signs, diagnosis, and non-surgical rehabilitation steps for athletic pubalgia (sports hernia) to get back on the field safely.',
                'meta_title': 'Sports Hernia Physical Therapy & Recovery Guide | Upfront',
                'meta_description': 'Understand symptoms and non-surgical recovery pathways for athletic pubalgia with professional sports physiotherapy.',
                'reading_time_minutes': 8,
                'is_featured': True,
                'body': '''<p>A <strong>sports hernia</strong> (technically known as <em>athletic pubalgia</em>) is a painful soft-tissue injury that occurs in the groin area. Unlike a classic abdominal hernia, there is no visible bulge, but the chronic groin pain can completely sideline athletes.</p>

<h2>What is a Sports Hernia?</h2>
<p>Athletic pubalgia is a strain or tear of any soft tissue (muscle, tendon, ligament) in the lower abdomen or groin area. It most commonly occurs in sports that involve sudden changes of direction, twisting movements, and intense kicking—such as football, rugby, and basketball.</p>

<h3>Key Symptoms</h3>
<ul>
<li>Sharp groin pain during twisting, sprinting, or kicking</li>
<li>A dull ache in the groin area after athletic activity</li>
<li>Pain that resolves with rest but returns immediately upon starting sports</li>
<li>Tenderness when pressing on the pubic bone</li>
</ul>

<h2>The Physical Therapy Rehabilitation Pathway</h2>
<p>For most athletes, a structured, conservative <strong>6 to 8-week physical therapy program</strong> is the first line of defense. Our specialized <a href="/services/page/sports-rehabilitation/">Sports Rehabilitation program</a> focuses on restoring muscular balance across the pelvis.</p>

<h3>Recommended Rehab Phases</h3>
<ol>
<li><strong>Phase 1: Pain Reduction & Protection</strong> — Gentle core activation, pelvic stabilization, and avoiding movements that trigger sharp groin pain.</li>
<li><strong>Phase 2: Core and Hip Strengthening</strong> — Strengthening the deep abdominals, glutes, and hip adductors to relieve stress on the pubic joint.</li>
<li><strong>Phase 3: Dynamic Movement & Plyometrics</strong> — Introducing rotational movement, light jumping, and sport-specific agility drills.</li>
</ol>

<h2>Preventing Re-injury</h2>
<p>Core stability and adductor flexibility are crucial. Regular dynamic stretching, proper warm-ups, and core exercises like planks and deadbugs can prevent groin strains. Explore our <a href="/services/page/general-wellness/">General Wellness tips</a> to stay active and injury-free.</p>

<p>Experiencing chronic groin pain? <a href="/accounts/signup/">Sign up for an assessment</a> to receive a personalized sports rehab evaluation today.</p>''',
            },
            # --- Spine & Joint Health ---
            {
                'title': 'The Complete Guide to Post-Operative Knee Replacement Rehabilitation',
                'slug': 'post-operative-knee-replacement-rehab',
                'category_slug': 'spine-joint-health',
                'excerpt': 'A week-by-week physical therapy guide to restoring mobility, reducing swelling, and gaining strength after total knee arthroplasty.',
                'meta_title': 'Post-Operative Total Knee Replacement Rehab Guide | Upfront',
                'meta_description': 'Recover quickly from total knee replacement with this week-by-week physical therapy guide to exercise, mobility, and swelling reduction.',
                'reading_time_minutes': 10,
                'is_featured': False,
                'body': '''<p>A <strong>Total Knee Replacement (TKA)</strong> is a life-changing procedure that eliminates chronic arthritis pain. However, the success of the surgery depends heavily on your post-operative physical therapy rehabilitation.</p>

<h2>Immediate Post-Surgery (Weeks 1-2)</h2>
<p>Rehab begins the day after surgery. The primary goals are managing swelling, extending the knee fully, and initiating safe weight-bearing exercises.</p>
<ul>
<li><strong>Knee Extension:</strong> Achieving a completely straight knee is critical for normal walking.</li>
<li><strong>Ankle Pumps & Quad Sets:</strong> Essential to prevent blood clots and wake up the quadriceps muscle.</li>
<li><strong>Walking:</strong> Practicing gait mechanics with a walker or crutches.</li>
</ul>

<h2>Gaining Range of Motion (Weeks 3-6)</h2>
<p>During this phase, we transition to cane assistance or unassisted walking. We aim for at least 110-120 degrees of knee flexion (bending).</p>
<ul>
<li><strong>Stationary Cycling:</strong> Excellent for improving knee bend and promoting blood circulation.</li>
<li><strong>Step-Ups & Squats:</strong> Restoring daily functional strength to climb stairs and stand up easily.</li>
<li><strong>Manual Therapy:</strong> Certified therapist Dan Mwangi Gichobi performs patellar mobilizations and scar tissue release.</li>
</ul>

<h2>Advanced Strengthening & Balance (Weeks 7-12)</h2>
<p>Focus shifts to long-term joint stability, balance training, and returning to recreational activities like hiking or swimming. See our <a href="/services/page/orthopedic-care/">Orthopedic Care clinic details</a> for customized program designs.</p>

<p>Ready to start your recovery? <a href="/accounts/signup/">Create a patient profile</a> to book your home or clinic sessions.</p>''',
            },
            # --- Lifestyle & Ergonomics ---
            {
                'title': '5 Ergonomic Tips to Prevent Back Pain When Working from Home in Kenya',
                'slug': 'ergonomic-tips-prevent-back-pain-wfh',
                'category_slug': 'lifestyle-ergonomics',
                'excerpt': 'Practical workspace setup and posture tips specifically designed for remote workers in Kenya to reduce spinal strain and neck pain.',
                'meta_title': 'Prevent WFH Back Pain: 5 Ergonomic Tips | Upfront',
                'meta_description': 'Practical workspace setup guidelines for remote workers in Kenya. Avoid lower back strain and neck fatigue with these ergonomic tips.',
                'reading_time_minutes': 5,
                'is_featured': False,
                'body': '''<p>With more Kenyans working remotely, there has been a significant surge in neck stiffness, shoulder tension, and chronic lower back pain. Many of these issues stem from poor ergonomics and sitting on unsupportive furniture.</p>

<h2>1. Adjust Your Chair Height</h2>
<p>Your feet should rest flat on the floor, with your knees bent at a 90-degree angle. If your chair is too high, use a footrest. Your hips should be slightly higher than or level with your knees.</p>

<h2>2. Provide Lumbar Support</h2>
<p>If your chair doesn\'t have built-in lower back support, roll up a small towel and place it behind the curve of your lower back. This helps maintain the natural inward curve of your spine.</p>

<h2>3. Position Your Screen at Eye Level</h2>
<p>Avoid looking down at your laptop, which places immense strain on your neck muscles. Raise your laptop using a stand or a stack of books, and use an external keyboard and mouse.</p>

<h2>4. The 20-20-20 Rule for Physical Rest</h2>
<p>Every 20 minutes, stand up for 20 seconds, and stretch. Movement is the best antidote to static muscle fatigue. Explore our <a href="/services/page/general-wellness/">Lifestyle Ergonomic services</a> for posture evaluations.</p>

<h2>5. Keep Essential Items Within Reach</h2>
  <p>Place your phone, notebook, and water bottle close to your body to prevent repetitive over-reaching, which causes muscle imbalances in the shoulders.</p>

<p>Need a professional posture analysis? <a href="/accounts/signup/">Schedule an ergonomic assessment</a> with Upfront today.</p>''',
            },
            # --- Neurological Recovery ---
            {
                'title': 'Stroke Rehabilitation: How Physiotherapy Restores Mobility and Independence',
                'slug': 'stroke-rehab-mobility-independence',
                'category_slug': 'neuro-recovery',
                'excerpt': 'Discover how neuro-physiotherapy, balance training, and repetitive movement therapies help stroke survivors recover motor functions.',
                'meta_title': 'Neuro-Physiotherapy for Stroke Rehabilitation | Upfront',
                'meta_description': 'Learn how specialized stroke rehabilitation and motor-learning exercises help stroke survivors regain balance, strength, and mobility.',
                'reading_time_minutes': 9,
                'is_featured': False,
                'body': '''<p>A stroke can damage the neural pathways connecting the brain and muscles, leading to muscle weakness, paralysis, or balance loss on one side of the body. Specialized <strong>neurological physiotherapy</strong> utilizes the brain\'s natural ability to reorganize itself (neuroplasticity) to restore movement.</p>

<h2>The Power of Neuroplasticity</h2>
<p>Through repetitive, task-specific exercises, the brain can build new pathways around the damaged areas. The sooner stroke rehabilitation begins, the better the recovery outcomes.</p>

<h3>Key Focus Areas in Stroke Rehab</h3>
<ol>
<li><strong>Gait Training:</strong> Helping the patient relearn how to walk safely, often using parallel bars, mirror feedback, and gait aids.</li>
<li><strong>Balance and Coordination:</strong> Exercises designed to improve core stability and prevent falls.</li>
<li><strong>Constraint-Induced Movement Therapy (CIMT):</strong> Encouraging the use of the weaker limb by temporarily restricting the stronger one.</li>
</ol>

<h2>Home-Based Stroke Care in Kenya</h2>
<p>For stroke survivors, traveling to a clinic can be incredibly exhausting. Our <a href="/services/page/stroke-rehabilitation/">Stroke and Neurological Rehab clinic</a> provides dedicated home-based visits to ensure recovery happens in a comfortable, familiar environment.</p>

<p>Learn more about our <a href="/faqs/">frequently asked stroke rehab questions</a> or sign up to consult Dan Mwangi Gichobi.</p>''',
            },
            # --- Success Stories ---
            {
                'title': 'From Injury to Marathon: How Proper Rehab Saved Mwangi\'s Running Career',
                'slug': 'mwangi-marathon-injury-rehab-success',
                'category_slug': 'success-stories',
                'excerpt': 'A client success story of recovery from a severe Achilles tendon tear through structured physical therapy with Dan Mwangi Gichobi.',
                'meta_title': 'Patient Story: Recovering from Achilles Tear | Upfront',
                'meta_description': 'Read how runner Mwangi recovered from a full Achilles tendon tear through sports physical therapy with Dan Mwangi Gichobi and returned to marathons.',
                'reading_time_minutes': 7,
                'is_featured': False,
                'body': '''<p>"When I tore my Achilles tendon during training, I was devastated. Doctors told me I might never run competitive marathons again. But working with Dan Mwangi Gichobi changed everything."</p>

<h2>The Diagnosis</h2>
<p>Mwangi, a passionate long-distance runner from Nakuru, suffered a severe Achilles tendon rupture. After undergoing surgical repair, his leg was immobilized in a cast for weeks, leaving him with severe muscle atrophy, stiffness, and fear of re-rupture.</p>

<h2>The Structured Rehabilitation</h2>
<p>Mwangi\'s recovery began with gentle joint mobilization and tendon loading. "Dan was extremely patient. He monitored my tendon recovery, making sure we loaded the muscle progressive without overloading the healing tendon."</p>

<p>The rehab incorporated eccentric heel drops, balance board exercises, and deep tissue mobilization. We slowly integrated running drills using our <a href="/services/page/sports-rehabilitation/">Sports Rehabilitation protocols</a>.</p>

<h2>Back on the Track</h2>
<p>Ten months post-injury, Mwangi successfully completed the Nairobi Marathon, achieving a personal best time. "The personalized care, expert manual therapy, and mental encouragement I received at Upfront made all the difference."</p>

<p>Ready to reclaim your active lifestyle? <a href="/accounts/signup/">Start your rehab journey with Upfront today</a>.</p>''',
            },
        ]

        for i, post_data in enumerate(posts):
            cat_slug = post_data.pop('category_slug')
            category = BlogCategory.objects.get(slug=cat_slug)
            post_data['category'] = category
            post_data['author'] = author
            post_data['status'] = 'PUBLISHED'
            post_data['published_at'] = now - timezone.timedelta(days=i * 3)

            post, created = BlogPost.objects.update_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            st = 'Created' if created else 'Updated'
            self.stdout.write(f"  {st} post: {post.title}")

    def _update_local_page_metadata(self):
        """Ensure every LocalPage has meta_title and meta_description filled."""
        pages = LocalPage.objects.all()
        for page in pages:
            changed = False
            if not page.meta_title:
                page.meta_title = f"{page.title} — Upfront"[:70]
                changed = True
            if not page.meta_description:
                page.meta_description = (page.hero_subheadline or page.title)[:160]
                changed = True
            if changed:
                page.save()
                self.stdout.write(f"  Updated metadata: {page.title}")
        self.stdout.write(f"  Checked {pages.count()} LocalPages for metadata.")
