from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from voting.models import Candidate, Election
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up the voting system with initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-admin',
            action='store_true',
            help='Create a default admin user',
        )
        parser.add_argument(
            '--create-candidates',
            action='store_true',
            help='Create sample candidates',
        )
        parser.add_argument(
            '--create-election',
            action='store_true',
            help='Create a sample election',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up Online Voting System...')
        )

        if options['create_admin']:
            self.create_admin_user()

        if options['create_candidates']:
            self.create_sample_candidates()

        if options['create_election']:
            self.create_sample_election()

        self.stdout.write(
            self.style.SUCCESS('Voting system setup completed!')
        )

    def create_admin_user(self):
        """Create a default admin user"""
        try:
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@votingsystem.com',
                    password='admin123',
                    full_name='System Administrator',
                    is_admin=True,
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(
                    self.style.SUCCESS('Admin user created successfully!')
                )
                self.stdout.write(
                    self.style.WARNING('   Username: admin')
                )
                self.stdout.write(
                    self.style.WARNING('   Password: admin123')
                )
                self.stdout.write(
                    self.style.WARNING('   Email: admin@votingsystem.com')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Admin user already exists')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )

    def create_sample_candidates(self):
        """Create sample candidates"""
        sample_candidates = [
            {
                'name': 'Rajesh Kumar',
                'description': 'Indian National Congress',
            },
            {
                'name': 'Priya Sharma',
                'description': 'Bharatiya Janata Party',
            },
            {
                'name': 'Amit Singh',
                'description': 'Aam Aadmi Party',
            },
            {
                'name': 'Sunita Devi',
                'description': 'Independent Candidate',
            },
        ]

        created_count = 0
        for candidate_data in sample_candidates:
            candidate, created = Candidate.objects.get_or_create(
                name=candidate_data['name'],
                defaults=candidate_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created candidate: {candidate.name}')
                )

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Created {created_count} sample candidates')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Sample candidates already exist')
            )

    def create_sample_election(self):
        """Create a sample election"""
        try:
            if not Election.objects.exists():
                now = timezone.now()
                election = Election.objects.create(
                    title='General Election 2024',
                    description='Democratic election for selecting representatives',
                    start_date=now,
                    end_date=now + timedelta(days=30),
                    is_active=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created election: {election.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Election already exists')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating election: {e}')
            )