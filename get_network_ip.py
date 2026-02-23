#!/usr/bin/env python3
"""
Network IP Address Finder for Android Access
Automatically finds your computer's IP address for mobile access
"""

import socket
import subprocess
import sys
import platform

def get_network_ip():
    """Get the network IP address of this computer"""
    try:
        # Method 1: Connect to external address to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Method 2: Get hostname IP
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None

def get_all_network_interfaces():
    """Get all network interfaces and their IP addresses"""
    interfaces = []
    
    try:
        if platform.system() == "Windows":
            # Windows ipconfig command
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            current_adapter = ""
            for line in lines:
                line = line.strip()
                if "adapter" in line.lower() and ":" in line:
                    current_adapter = line
                elif "IPv4 Address" in line and ":" in line:
                    ip = line.split(":")[-1].strip()
                    if not ip.startswith("127.") and ip != "":
                        interfaces.append((current_adapter, ip))
        
        else:
            # Unix/Linux/Mac ifconfig command
            try:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            except FileNotFoundError:
                # Try ip command on newer Linux systems
                result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            
            lines = result.stdout.split('\n')
            current_interface = ""
            
            for line in lines:
                if line and not line.startswith(' ') and not line.startswith('\t'):
                    current_interface = line.split(':')[0]
                elif 'inet ' in line and '127.0.0.1' not in line:
                    parts = line.split()
                    for part in parts:
                        if part.startswith('inet'):
                            ip = part.split('inet')[-1].split('/')[0].strip()
                            if ip and not ip.startswith('127.'):
                                interfaces.append((current_interface, ip))
                            break
    
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
    
    return interfaces

def main():
    print("🌐 Network IP Address Finder for Android Access")
    print("=" * 55)
    
    # Get primary network IP
    primary_ip = get_network_ip()
    
    if primary_ip:
        print(f"📱 PRIMARY IP ADDRESS: {primary_ip}")
        print(f"🔗 Android Access URL: http://{primary_ip}:8000")
        print()
    
    # Get all network interfaces
    print("📋 All Network Interfaces:")
    print("-" * 30)
    
    interfaces = get_all_network_interfaces()
    
    if interfaces:
        for interface, ip in interfaces:
            print(f"Interface: {interface}")
            print(f"IP Address: {ip}")
            print(f"Access URL: http://{ip}:8000")
            print("-" * 30)
    else:
        print("No network interfaces found or error occurred.")
        print("Try running 'ipconfig' (Windows) or 'ifconfig' (Mac/Linux) manually.")
    
    print()
    print("🚀 QUICK SETUP INSTRUCTIONS:")
    print("=" * 55)
    print("1. Start Django server with network access:")
    print("   python manage.py runserver 0.0.0.0:8000")
    print()
    print("2. On your Android device, open browser and go to:")
    if primary_ip:
        print(f"   http://{primary_ip}:8000")
    else:
        print("   http://YOUR_IP_ADDRESS:8000")
    print()
    print("3. Make sure both devices are on the same WiFi network!")
    print()
    print("🔧 TROUBLESHOOTING:")
    print("- If connection fails, check Windows Firewall settings")
    print("- Try different IP addresses listed above")
    print("- Ensure both devices are on same WiFi network")
    print("- Try using port 8080 if 8000 doesn't work")

if __name__ == "__main__":
    main()