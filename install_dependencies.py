#!/usr/bin/env python3
"""
Dependency Installation Script for Django Voting System
This script tries different approaches to install required packages.
"""

import subprocess
import sys
import os

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

def install_packages():
    """Try different approaches to install packages"""
    print("Installing Django Voting System Dependencies")
    print("=" * 60)
    
    # Try main requirements first
    print("\n📦 Attempting to install main requirements...")
    if run_command("pip install -r requirements.txt", "Installing main requirements"):
        print("✅ All packages installed successfully!")
        return True
    
    print("\n⚠️  Main installation failed. Trying alternative approach...")
    
    # Try alternative requirements
    if run_command("pip install -r requirements-alternative.txt", "Installing alternative requirements"):
        print("✅ Alternative packages installed successfully!")
        print("\n📝 Note: Using PyMySQL instead of mysqlclient")
        return True
    
    print("\n⚠️  Alternative installation failed. Trying individual packages...")
    
    # Try installing packages individually
    packages = [
        "Django==4.2.7",
        "django-crispy-forms==2.1", 
        "crispy-bootstrap5==0.7"
    ]
    
    success_count = 0
    for package in packages:
        if run_command(f"pip install {package}", f"Installing {package}"):
            success_count += 1
    
    if success_count == len(packages):
        print("✅ Core packages installed successfully!")
        
        # Try to install database connector
        print("\n🗄️  Installing database connector...")
        if run_command("pip install mysqlclient", "Installing mysqlclient"):
            print("✅ MySQL connector installed!")
        elif run_command("pip install PyMySQL", "Installing PyMySQL as alternative"):
            print("✅ Alternative MySQL connector installed!")
        else:
            print("⚠️  No MySQL connector installed. Will use SQLite for development.")
        
        return True
    
    print("❌ Failed to install required packages!")
    return False

def main():
    """Main function"""
    if install_packages():
        print("\nInstallation completed!")
        print("\nNext steps:")
        print("1. Run: python run_django.py")
        print("2. Or manually: python manage.py runserver")
        print("\nApplication will be available at: http://localhost:8000")
    else:
        print("\nInstallation failed!")
        print("\nTroubleshooting:")
        print("1. Make sure you have Python 3.8+ installed")
        print("2. Try upgrading pip: python -m pip install --upgrade pip")
        print("3. Consider using a virtual environment")
        print("4. For MySQL issues, install MySQL development headers")
        sys.exit(1)

if __name__ == "__main__":
    main()