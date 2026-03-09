#!/usr/bin/env python3
"""
MySQL Database Setup Script
Creates the voting_system database
"""

import pymysql
import sys

def create_database():
    """Create MySQL database for voting system"""
    try:
        # Connect to MySQL server (without database)
        print("🔌 Connecting to MySQL server...")
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected to MySQL server!")
        
        with connection.cursor() as cursor:
            # Create database
            print("📊 Creating database 'voting_system'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS voting_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'voting_system' created successfully!")
            
            # Grant privileges
            print("🔐 Granting privileges...")
            cursor.execute("GRANT ALL PRIVILEGES ON voting_system.* TO 'root'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privileges granted!")
            
            # Show databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\n📋 Available databases:")
            for db in databases:
                db_name = db['Database']
                if db_name == 'voting_system':
                    print(f"  ✓ {db_name} (READY)")
                else:
                    print(f"    {db_name}")
        
        connection.close()
        print("\n🎉 MySQL setup complete!")
        print("\n📝 Next steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py setup_voting --create-admin --create-candidates")
        print("3. Run: python manage.py runserver")
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ MySQL Connection Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check if password is correct (currently using 'root')")
        print("3. Try: mysql -u root -p")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  MySQL Database Setup for Voting System")
    print("=" * 60)
    print()
    
    success = create_database()
    sys.exit(0 if success else 1)
