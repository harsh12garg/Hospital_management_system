#!/usr/bin/env python
"""
Hospital Management System Setup Script
This script will:
1. Run database migrations
2. Create sample data for testing
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(e.stderr)
        return False

def main():
    print("🏥 Hospital Management System Setup")
    print("=" * 50)
    
    # Check if manage.py exists
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Run migrations first
    migration_commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Applying migrations"),
    ]
    
    print("📋 Step 1: Setting up database...")
    for command, description in migration_commands:
        if not run_command(command, description):
            print(f"❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n📋 Step 2: Creating sample data...")
    data_commands = [
        ("python create_simple_data.py", "Creating sample data"),
    ]
    
    for command, description in data_commands:
        if not run_command(command, description):
            print(f"❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 What's been created:")
    print("   • Database tables and relationships")
    print("   • Sample admin, doctors, and patients")
    print("   • Sample appointments and billing records")
    print("\n🔐 Login credentials:")
    print("   Admin: admin / admin123")
    print("   Doctor: dr_smith / doctor123")
    print("   Patient: patient1 / patient123")
    print("\n🚀 Start the server with: python manage.py runserver")

if __name__ == "__main__":
    main()