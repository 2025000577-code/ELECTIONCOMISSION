from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass

User = get_user_model()


class Command(BaseCommand):
    help = 'Create an admin user for the voting system'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Creating Admin User for Voting System')
        )
        self.stdout.write('=' * 50)

        # Get username
        username = options['username']
        if not username:
            username = input('Username: ').strip()
            if not username:
                username = 'admin'

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User with username "{username}" already exists!')
            )
            return

        # Get email
        email = options['email']
        if not email:
            email = input('Email: ').strip()
            if not email:
                email = f'{username}@votingsystem.com'

        # Get full name
        full_name = input('Full Name: ').strip()
        if not full_name:
            full_name = 'System Administrator'

        # Get password
        password = options['password']
        if not password:
            password = getpass.getpass('Password: ')
            if not password:
                password = 'admin123'
                self.stdout.write(
                    self.style.WARNING('Using default password: admin123')
                )

        try:
            # Create admin user
            admin_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                is_admin=True,
                is_staff=True,
                is_superuser=True
            )

            self.stdout.write(
                self.style.SUCCESS('Admin user created successfully!')
            )
            self.stdout.write(f'   Username: {admin_user.username}')
            self.stdout.write(f'   Email: {admin_user.email}')
            self.stdout.write(f'   Full Name: {admin_user.full_name}')
            self.stdout.write('')
            self.stdout.write(
                self.style.SUCCESS('You can now login to the admin panel!')
            )
            self.stdout.write('   Admin Login: /admin/login/')
            self.stdout.write('   Voting Admin: /admin/login/')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )