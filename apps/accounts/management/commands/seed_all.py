from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs all available seed commands sequentially to populate the database'

    def handle(self, *args, **kwargs):
        commands_to_run = [
            'seed_courses',
            'seed_milestones',
            'seed_homepage',
            'seed_footer',
            'seed_blog_content',
            'seed_all_links',
        ]

        for command_name in commands_to_run:
            self.stdout.write(self.style.WARNING(f"\n--- Running: {command_name} ---"))
            try:
                call_command(command_name)
                self.stdout.write(self.style.SUCCESS(f"Successfully ran {command_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error running {command_name}: {e}"))

        self.stdout.write(self.style.SUCCESS("\nAll seeding completed!"))
