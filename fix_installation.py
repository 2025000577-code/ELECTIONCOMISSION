#!/usr/bin/env python3
"""
Quick Fix Installation Script
Handles common installation issues on Windows
"""

import subprocess
import sys
import os

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

def main():
    print("🚀 Quick Fix Installation")
    print("=" * 40)
    
    # Update pip first
    print("📦 Updating pip...")
    run_command("python -m pip install --upgrade pip", "Updating pip")
    
    # Install packages one by one
    packages = [
        "Django==4.2.7",
        "django-crispy-forms==2.1", 
        "crispy-bootstrap5==0.7",
        "python-dotenv==1.0.0"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")
    
    # Try to install Pillow with different methods
    print("\n🖼️  Installing Pillow (image support)...")
    pillow_methods = [
        "pip install Pillow",
        "pip install --upgrade Pillow",
        "pip install Pillow --no-cache-dir",
        "pip install Pillow==9.5.0"
    ]
    
    pillow_installed = False
    for method in pillow_methods:
        if run_command(method, f"Trying: {method}"):
            pillow_installed = True
            break
    
    if not pillow_installed:
        print("⚠️  Pillow installation failed. ID verification will be disabled.")
        print("💡 You can continue without image support for now.")
    
    print("\n" + "=" * 40)
    print("🎉 Installation complete!")
    print("\n📋 Next steps:")
    print("1. Run: python manage.py migrate")
    print("2. Run: python manage.py setup_voting --create-admin")
    print("3. Run: python manage.py runserver")

if __name__ == "__main__":
    main()