#!/usr/bin/env python3
"""
Environment Setup Script for Online Voting System
Automatically sets up the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    if not os.path.exists('venv'):
        print("🔧 Creating virtual environment...")
        if run_command('python -m venv venv', "Creating virtual environment"):
            print("✅ Virtual environment created")
            return True
        return False
    else:
        print("✅ Virtual environment already exists")
        return True

def activate_virtual_environment():
    """Instructions for activating virtual environment"""
    if os.name == 'nt':  # Windows
        activate_script = 'venv\\Scripts\\activate.bat'
        print(f"💡 To activate virtual environment, run: {activate_script}")
    else:  # Unix/Linux/Mac
        activate_script = 'source venv/bin/activate'
        print(f"💡 To activate virtual environment, run: {activate_script}")

def install_dependencies():
    """Install Python dependencies"""
    pip_command = 'venv\\Scripts\\pip' if os.name == 'nt' else 'venv/bin/pip'
    
    if not os.path.exists(pip_command.split('\\')[0] if os.name == 'nt' else pip_command.split('/')[0]):
        pip_command = 'pip'  # Fallback to system pip
    
    return run_command(f'{pip_command} install -r requirements.txt', "Installing dependencies")

def setup_environment_file():
    """Set up .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
        else:
            print("⚠️  .env.example not found, creating basic .env file")
            with open('.env', 'w') as f:
                f.write("""# Django Configuration
SECRET_KEY=django-insecure-voting-system-dev-key-2024
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*

# Database Configuration
DB_ENGINE=sqlite

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
""")
            print("✅ Created basic .env file")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    directories = ['media', 'media/id_proofs', 'logs', 'staticfiles']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_migrations():
    """Run Django migrations"""
    python_command = 'venv\\Scripts\\python' if os.name == 'nt' else 'venv/bin/python'
    
    if not os.path.exists(python_command.split('\\')[0] if os.name == 'nt' else python_command.split('/')[0]):
        python_command = 'python'  # Fallback to system python
    
    commands = [
        (f'{python_command} manage.py makemigrations', "Creating migrations"),
        (f'{python_command} manage.py migrate', "Applying migrations"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_superuser():
    """Create admin user"""
    python_command = 'venv\\Scripts\\python' if os.name == 'nt' else 'venv/bin/python'
    
    if not os.path.exists(python_command.split('\\')[0] if os.name == 'nt' else python_command.split('/')[0]):
        python_command = 'python'
    
    print("🔧 Creating admin user and sample data...")
    return run_command(f'{python_command} manage.py setup_voting --create-admin --create-candidates', 
                      "Creating admin user and sample data")

def main():
    """Main setup function"""
    print("🚀 Online Voting System - Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Show activation instructions
    activate_virtual_environment()
    
    # Install dependencies
    print("\n📦 Installing Dependencies...")
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        print("💡 Try running: pip install -r requirements.txt")
        return False
    
    # Setup environment file
    print("\n⚙️  Setting up environment...")
    setup_environment_file()
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Run migrations
    print("\n🗄️  Setting up database...")
    if not run_migrations():
        print("❌ Failed to run migrations")
        return False
    
    # Create admin user
    print("\n👤 Setting up admin user...")
    if not create_superuser():
        print("⚠️  Failed to create admin user automatically")
        print("💡 You can create it manually later with: python manage.py setup_voting --create-admin")
    
    print("\n" + "=" * 50)
    print("🎉 Environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate.bat")
    else:
        print("   source venv/bin/activate")
    print("2. Start the development server:")
    print("   python manage.py runserver")
    print("3. For Android access:")
    print("   python start_for_android.py")
    print("\n🔑 Default admin credentials:")
    print("   Email: admin@votingsystem.com")
    print("   Password: admin123")
    print("\n🌐 Access URLs:")
    print("   Home: http://localhost:8000/")
    print("   Admin: http://localhost:8000/voting-admin/login/")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)