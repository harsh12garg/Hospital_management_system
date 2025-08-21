#!/usr/bin/env python
"""
Simple Fix Script - Bypasses admin issues
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')

def setup_database():
    """Setup database without admin checks"""
    print("🔄 Setting up database...")
    
    # Import Django and setup
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    try:
        # Create migrations
        print("Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'hospital', '--verbosity=0'])
        print("✅ Migrations created")
        
        # Apply migrations
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
        print("✅ Migrations applied")
        
        return True
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def create_sample_data():
    """Create sample data"""
    print("🔄 Creating sample data...")
    
    try:
        from django.contrib.auth.models import User
        from hospital.models import Doctor, Patient, Appointment, Billing, UserProfile
        from datetime import date, timedelta
        import random
        
        # Create admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@hospital.com',
                password='admin123',
                first_name='John',
                last_name='Administrator'
            )
            UserProfile.objects.create(user=admin_user, role='admin', phone='+1-555-0001')
            print("✅ Admin created")
        
        # Create a doctor
        if not User.objects.filter(username='dr_smith').exists():
            doctor_user = User.objects.create_user(
                username='dr_smith',
                email='dr.smith@hospital.com',
                password='doctor123',
                first_name='Sarah',
                last_name='Smith'
            )
            UserProfile.objects.create(user=doctor_user, role='doctor', phone='+1-555-0101')
            Doctor.objects.create(
                user=doctor_user,
                specialization='cardiology',
                experience_years=15,
                consultation_fee=200.00,
                is_available=True
            )
            print("✅ Doctor created")
        
        # Create a patient
        if not User.objects.filter(username='patient1').exists():
            patient_user = User.objects.create_user(
                username='patient1',
                email='patient1@email.com',
                password='patient123',
                first_name='Alice',
                last_name='Cooper'
            )
            UserProfile.objects.create(user=patient_user, role='patient', phone='+1-555-1001')
            Patient.objects.create(
                user=patient_user,
                patient_id='PAT10001',
                blood_group='A+',
                emergency_contact='+1-555-2001'
            )
            print("✅ Patient created")
        
        # Create an appointment
        doctor = Doctor.objects.first()
        patient = Patient.objects.first()
        
        if doctor and patient and not Appointment.objects.filter(doctor=doctor, patient=patient).exists():
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                appointment_date=date.today() + timedelta(days=1),
                appointment_time='10:00',
                reason='Regular checkup',
                status='scheduled'
            )
            print("✅ Appointment created")
            
            # Create billing
            if not Billing.objects.filter(appointment=appointment).exists():
                Billing.objects.create(
                    appointment=appointment,
                    total_amount=doctor.consultation_fee,
                    payment_status='pending'
                )
                print("✅ Billing record created")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample data error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔧 Simple Fix for Hospital Management System")
    print("=" * 50)
    
    # Step 1: Setup database
    if not setup_database():
        print("❌ Database setup failed")
        return
    
    # Step 2: Create sample data
    if not create_sample_data():
        print("❌ Sample data creation failed")
        return
    
    print("\n🎉 Simple fix completed successfully!")
    print("\n📋 Summary:")
    
    # Show summary
    try:
        from django.contrib.auth.models import User
        from hospital.models import Doctor, Patient, Appointment, Billing
        
        print(f"   • Users: {User.objects.count()}")
        print(f"   • Doctors: {Doctor.objects.count()}")
        print(f"   • Patients: {Patient.objects.count()}")
        print(f"   • Appointments: {Appointment.objects.count()}")
        print(f"   • Bills: {Billing.objects.count()}")
    except:
        pass
    
    print("\n🚀 You can now run: python manage.py runserver")
    print("\n🔐 Login with:")
    print("   Admin: admin / admin123")
    print("   Doctor: dr_smith / doctor123")
    print("   Patient: patient1 / patient123")

if __name__ == "__main__":
    main()