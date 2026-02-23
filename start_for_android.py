#!/usr/bin/env python3
"""
Android-Ready Django Server Starter
Automatically configures and starts Django server for Android access
"""

import os
import sys
import socket
import subprocess
import platform
import time

def get_network_ip():
    """Get the network IP address of this computer"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "Unable to determine IP"

def check_port_available(port):
    """Check if a port is available"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.close()
        return True
    except OSError:
        return False

def setup_django():
    """Setup Django database and admin user if needed"""
    print("🔧 Setting up Django...")
    
    # Check if database exists
    if not os.path.exists('db.sqlite3'):
        print("📊 Creating database...")
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
        
        print("👤 Creating admin user...")
        os.system('python manage.py setup_voting --create-admin --create-candidates')
    else:
        print("✅ Database already exists")
    
    print("✅ Django setup complete!")

def check_firewall_warning():
    """Show firewall warning for Windows users"""
    if platform.system() == "Windows":
        print()
        print("🔥 WINDOWS FIREWALL NOTICE:")
        print("=" * 40)
        print("If you get a Windows Firewall popup, click 'Allow access'")
        print("This allows your Android device to connect to the server.")
        print()

def main():
    print("🚀 Android-Ready Django Server Starter")
    print("=" * 50)
    
    # Get network IP
    network_ip = get_network_ip()
    print(f"📱 Your computer's IP address: {network_ip}")
    
    # Find available port
    port = 8000
    if not check_port_available(port):
        print(f"⚠️  Port {port} is busy, trying port 8080...")
        port = 8080
        if not check_port_available(port):
            print(f"⚠️  Port {port} is also busy, trying port 8888...")
            port = 8888
    
    print(f"🌐 Using port: {port}")
    
    # Setup Django if needed
    setup_django()
    
    # Show firewall warning
    check_firewall_warning()
    
    # Display access information
    print()
    print("📱 ANDROID ACCESS INFORMATION:")
    print("=" * 50)
    print(f"🔗 URL for Android: http://{network_ip}:{port}")
    print()
    print("📋 INSTRUCTIONS:")
    print("1. Make sure your Android device is on the same WiFi network")
    print("2. Open any browser on your Android device")
    print(f"3. Go to: http://{network_ip}:{port}")
    print("4. Enjoy your mobile-optimized voting system!")
    print()
    print("🔑 ADMIN CREDENTIALS:")
    print("   Email: admin@votingsystem.com")
    print("   Password: admin123")
    print()
    print("🚀 Starting Django server...")
    print("=" * 50)
    
    # Start Django server
    try:
        cmd = f'python manage.py runserver 0.0.0.0:{port}'
        print(f"Running: {cmd}")
        print()
        
        # Show final access URL
        print("🎉 SERVER STARTED SUCCESSFULLY!")
        print(f"📱 Android Access: http://{network_ip}:{port}")
        print("💻 Local Access: http://localhost:{port}")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        os.system(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Make sure you're in the project directory")
        print("2. Check if Python and Django are installed")
        print("3. Try running: python manage.py runserver 0.0.0.0:8000")

if __name__ == "__main__":
    main()