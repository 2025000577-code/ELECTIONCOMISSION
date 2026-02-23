#!/usr/bin/env python3
"""
Database Setup Script for Django Online Voting System
This script helps set up MySQL database for Django.
"""

import mysql.connector
from mysql.connector import Error
import getpasst
import sys
import os

def get_mysql_credentials():
    """Get MySQL credentials from user"""
    print("MySQL Database Setup for Django")
    print("-" * 40)
    
    host = input("MySQL Host (default: localhost): ").strip() or 'localhost'
    user = input("MySQL Username (default: root): ").strip() or 'root'
    
    # Try common password scenarios
    print("\nTrying to connect to MySQL...")
    
    # First try with no password
    try:
        connection = mysql.connector.connect(
            host=localhost,
            user=root,
            password='root'
        )
        connection.close()
        print("✓ Connected successfully with no password")
        return {'host': host, 'user': user, 'password': ''}
    except Error:
        pass
    
    # Try with common default passwords
    common_passwords = ['password', 'root', '123456', 'mysql']
    for pwd in common_passwords:
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=pwd
            )
            connection.close()
            print(f"✓ Connected successfully with password: {pwd}")
            return {'host': host, 'user': user, 'password': pwd}
        except Error:
            continue
    
    # Ask user for password
    while True:
        password = getpass.getpass("MySQL Password: ")
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            connection.close()
            print("✓ Connected successfully!")
            return {'host': host, 'user': user, 'password': password}
        except Error as e:
            print(f"❌ Connection failed: {e}")
            retry = input("Try again? (y/n): ").lower().strip()
            if retry != 'y':
                return None

def create_database():
    """Create the voting system database"""
    # Get MySQL credentials
    db_config = get_mysql_credentials()
    if not db_config:
        print("❌ Could not connect to MySQL. Exiting...")
        return False
    
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        print("\n🗳️  Creating database...")
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS voting_system")
        print("✓ Database 'voting_system' created successfully!")
        
        connection.commit()
        
        # Save configuration for Django
        save_django_config(db_config)
        
        print("\n🎉 Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Update DATABASES setting in voting_system/settings.py if needed")
        print("2. Run: python manage.py makemigrations")
        print("3. Run: python manage.py migrate")
        print("4. Run: python manage.py setup_voting --create-admin --create-candidates")
        print("5. Run: python manage.py runserver")
        
        return True
        
    except Error as e:
        print(f"❌ Error: {e}")
        print("\nPlease make sure:")
        print("1. MySQL server is running")
        print("2. You have the correct credentials")
        print("3. You have necessary permissions")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed.")

def save_django_config(db_config):
    """Save database configuration for Django"""
    try:
        config_content = f"""# Database Configuration for Django (Auto-generated)
# Add these settings to your voting_system/settings.py DATABASES configuration

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'voting_system',
        'USER': '{db_config['user']}',
        'PASSWORD': '{db_config['password']}',
        'HOST': '{db_config['host']}',
        'PORT': '3306',
        'OPTIONS': {{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }},
    }}
}}

# Environment variables (recommended for production)
# DB_NAME=voting_system
# DB_USER={db_config['user']}
# DB_PASSWORD={db_config['password']}
# DB_HOST={db_config['host']}
# DB_PORT=3306
"""
        
        with open('django_db_config.py', 'w') as f:
            f.write(config_content)
        print("✓ Django database configuration saved to django_db_config.py")
    except Exception as e:
        print(f"⚠️  Could not save config file: {e}")

if __name__ == "__main__":
    print("🗳️  Django Online Voting System - Database Setup")
    print("=" * 60)
    
    success = create_database()
    if not success:
        sys.exit(1)