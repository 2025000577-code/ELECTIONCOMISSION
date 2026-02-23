#!/usr/bin/env python3
"""
Quick Setup Script for Django Voting System
This script handles the custom user model setup automatically.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description, ignore_errors=False):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"⚠️  {description} had issues (continuing anyway)")
            return True
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def setup_fresh_project():
    """Set up the project from scratch"""
    print("🗳️  Django Voting System - Quick Setup")
    print("=" * 50)
    
    # Check database configuration
    db_engine = os.environ.get('DB_ENGINE', 'sqlite')
    if db_engine.lower() == 'mysql':
        print("🗄️  Using MySQL database")
        print("   Make sure MySQL server is running and credentials are correct")
        print("   Set environment variables: DB_NAME, DB_USER, DB_PASSWORD")
    else:
        print("🗄️  Using SQLite database (default)")
        print("   Perfect for development and testing")
    
    # Remove existing migrations and database
    print("\n🧹 Cleaning up existing files...")
    
    # Remove migration files
    migrations_dir = Path("voting/migrations")
    if migrations_dir.exists():
        for file in migrations_dir.glob("0*.py"):
            file.unlink()
            print(f"✅ Removed {file}")
    
    # Remove SQLite database if exists
    db_file = Path("db.sqlite3")
    if db_file.exists():
        db_file.unlink()
        print("✅ Removed SQLite database")
    
    # Create fresh migrations
    print("\n� Creating fresh migrations...")
    if not run_command("python manage.py makemigrations voting", "Creating voting app migrations"):
        return False
    
    # Run migrations
    print("\n�️  Setting up database...")
    if not run_command("python manage.py migrate", "Running all migrations"):
        return False
    
    # Create admin user and sample data
    print("\n� Creating admin user and sample data...")
    if not run_command("python manage.py setup_voting --create-admin --create-candidates --create-election", 
                      "Setting up initial data"):
        print("⚠️  Initial data setup failed, but continuing...")
    
    # Collect static files
    print("\n� Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files", ignore_errors=True)
    
    print("\n🎉 Setup completed successfully!")
    print(f"\n🗄️  Database: {'MySQL' if db_engine.lower() == 'mysql' else 'SQLite'}")
    print("\n📍 You can now access:")
    print("   - Main app: http://localhost:8000/")
    print("   - Django admin: http://localhost:8000/admin/")
    print("   - Voting admin: http://localhost:8000/admin/login/")
    print("\n🔑 Default admin credentials:")
    print("   - Username: admin")
    print("   - Password: admin123")
    
    if db_engine.lower() != 'mysql':
        print("\n💡 To use MySQL instead of SQLite:")
        print("   1. Install MySQL server")
        print("   2. Set environment variable: DB_ENGINE=mysql")
        print("   3. Set DB_NAME, DB_USER, DB_PASSWORD as needed")
        print("   4. Run setup again")
    
    return True

def main():
    """Main function"""
    if setup_fresh_project():
        print("\n🚀 Starting development server...")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        try:
            subprocess.run("python manage.py runserver 0.0.0.0:8000", shell=True, check=True)
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped by user")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Server error: {e}")
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()