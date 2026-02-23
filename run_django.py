#!/usr/bin/env python3
"""
Django Voting System Startup Script
This script helps set up and run the Django voting system.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings')

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    try:
        import django
        import mysqlclient
        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_database():
    """Set up the database"""
    print("\n🗄️  Setting up database...")
    
    # Check if we need to reset migrations for custom user model
    migrations_dir = Path("voting/migrations")
    if migrations_dir.exists():
        migration_files = list(migrations_dir.glob("0*.py"))
        if migration_files:
            print("⚠️  Existing migrations found. Checking for custom user model compatibility...")
            choice = input("Reset migrations for custom user model? (recommended for first setup) (y/n): ").lower().strip()
            if choice == 'y':
                if not run_command("python reset_migrations.py", "Resetting migrations"):
                    return False
                return True
    
    # Run migrations normally
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Running migrations"):
        return False
    
    return True

def create_initial_data():
    """Create initial data"""
    print("\n👤 Setting up initial data...")
    
    # Create admin user and sample data
    if not run_command("python manage.py setup_voting --create-admin --create-candidates --create-election", 
                      "Creating initial data"):
        return False
    
    return True

def collect_static():
    """Collect static files"""
    print("\n📁 Collecting static files...")
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def run_server():
    """Run the Django development server"""
    print("\n🚀 Starting Django development server...")
    print("📍 Application will be available at: http://localhost:8000")
    print("👤 Admin panel: http://localhost:8000/admin/")
    print("🗳️  Voting system: http://localhost:8000/")
    print("🔑 Default admin credentials: admin / admin123")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run("python manage.py runserver 0.0.0.0:8000", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server error: {e}")

def main():
    """Main function"""
    print("🗳️  Django Online Voting System")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("\n❌ Database setup failed!")
        choice = input("Do you want to continue anyway? (y/n): ").lower().strip()
        if choice != 'y':
            sys.exit(1)
    
    # Create initial data
    create_initial_data()  # Continue even if this fails
    
    # Collect static files
    collect_static()  # Continue even if this fails
    
    # Run server
    run_server()

if __name__ == "__main__":
    main()