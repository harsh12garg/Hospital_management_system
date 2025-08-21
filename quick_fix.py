#!/usr/bin/env python
"""
Quick Fix Script for Hospital Management System
This will fix the current issues and set up the system properly.
"""

import os
import sys
import subprocess

def run_command(command, description, ignore_admin_errors=False):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.lower()
        if ignore_admin_errors and ('admin' in error_msg or 'billingadmin' in error_msg):
            print(f"⚠️  Admin error ignored: {description}")
            return True
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    print("🔧 Quick Fix for Hospital Management System")
    print("=" * 50)
    
    # Step 1: Create and apply migrations
    print("Step 1: Database setup...")
    if not run_command("python manage.py makemigrations hospital", "Creating migrations", ignore_admin_errors=True):
        print("⚠️  Continuing anyway...")
    
    if not run_command("python manage.py migrate", "Applying migrations", ignore_admin_errors=True):
        print("❌ Migration failed. Please check for errors.")
        return
    
    # Step 2: Create simple sample data
    print("\nStep 2: Creating sample data...")
    if not run_command("python create_simple_data.py", "Creating sample data"):
        print("❌ Sample data creation failed.")
        return
    
    print("\n🎉 Quick fix completed!")
    print("\n🚀 You can now run: python manage.py runserver")
    print("\n🔐 Login with:")
    print("   Admin: admin / admin123")
    print("   Doctor: dr_smith / doctor123")
    print("   Patient: patient1 / patient123")

if __name__ == "__main__":
    main()