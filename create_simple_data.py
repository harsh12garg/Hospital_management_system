#!/usr/bin/env python
"""
Simple Sample Data Generator for Hospital Management System
This version creates basic data that works with the current database schema.
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
django.setup()

from django.contrib.auth.models import User
from hospital.models import Doctor, Patient, Appointment, Billing, UserProfile

def create_admin():
    """Create admin user"""
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@hospital.com',
            password='admin123',
            first_name='John',
            last_name='Administrator'
        )
        UserProfile.objects.create(
            user=admin_user,
            role='admin',
            phone='+1-555-0001'
        )
        print("✓ Admin user created")
    else:
        print("✓ Admin user already exists")

def create_doctors():
    """Create sample doctors"""
    doctors_data = [
        ('dr_smith', 'Sarah', 'Smith', 'cardiology', 15, 200.00),
        ('dr_johnson', 'Michael', 'Johnson', 'neurology', 12, 250.00),
        ('dr_williams', 'Emily', 'Williams', 'pediatrics', 8, 180.00),
        ('dr_brown', 'David', 'Brown', 'orthopedics', 20, 300.00),
        ('dr_davis', 'Lisa', 'Davis', 'dermatology', 10, 220.00),
    ]
    
    for username, first_name, last_name, spec, exp, fee in doctors_data:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@hospital.com',
                password='doctor123',
                first_name=first_name,
                last_name=last_name
            )
            
            UserProfile.objects.create(
                user=user,
                role='doctor',
                phone=f'+1-555-010{random.randint(1,9)}'
            )
            
            Doctor.objects.create(
                user=user,
                specialization=spec,
                experience_years=exp,
                consultation_fee=fee,
                is_available=True
            )
            print(f"✓ Doctor {first_name} {last_name} created")
        else:
            print(f"✓ Doctor {first_name} {last_name} already exists")

def create_patients():
    """Create sample patients"""
    patients_data = [
        ('patient1', 'Alice', 'Cooper', 'A+'),
        ('patient2', 'Bob', 'Wilson', 'O-'),
        ('patient3', 'Carol', 'Martinez', 'B+'),
        ('patient4', 'Daniel', 'Garcia', 'AB+'),
        ('patient5', 'Eva', 'Rodriguez', 'O+'),
        ('patient6', 'Frank', 'Lee', 'A-'),
    ]
    
    for i, (username, first_name, last_name, blood_group) in enumerate(patients_data, 1):
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@email.com',
                password='patient123',
                first_name=first_name,
                last_name=last_name
            )
            
            UserProfile.objects.create(
                user=user,
                role='patient',
                phone=f'+1-555-100{i}'
            )
            
            Patient.objects.create(
                user=user,
                patient_id=f'PAT{10000 + i}',
                blood_group=blood_group,
                emergency_contact=f'+1-555-200{i}'
            )
            print(f"✓ Patient {first_name} {last_name} created")
        else:
            print(f"✓ Patient {first_name} {last_name} already exists")

def create_appointments():
    """Create sample appointments"""
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    
    if not doctors.exists() or not patients.exists():
        print("❌ No doctors or patients found. Create users first.")
        return
    
    appointment_reasons = [
        "Regular checkup",
        "Follow-up consultation", 
        "Chest pain evaluation",
        "Headache and dizziness",
        "Skin rash examination",
        "Joint pain assessment",
        "Routine physical exam",
        "Blood pressure monitoring",
        "Diabetes management",
        "Vaccination"
    ]
    
    statuses = ['scheduled', 'completed', 'cancelled']
    
    # Create 15 appointments
    created_count = 0
    for i in range(15):
        doctor = random.choice(doctors)
        patient = random.choice(patients)
        
        # Random date within next 30 days
        appointment_date = date.today() + timedelta(days=random.randint(-5, 25))
        
        # Random time during working hours
        hour = random.randint(9, 16)
        minute = random.choice([0, 15, 30, 45])
        appointment_time = f"{hour:02d}:{minute:02d}"
        
        # Check if appointment already exists
        existing = Appointment.objects.filter(
            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists()
        
        if not existing:
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=random.choice(appointment_reasons),
                status=random.choice(statuses),
                notes=f"Sample appointment for {patient.user.get_full_name()}"
            )
            created_count += 1
    
    print(f"✓ {created_count} appointments created")

def create_billing():
    """Create sample billing records"""
    completed_appointments = Appointment.objects.filter(status='completed')
    
    if not completed_appointments.exists():
        # Mark some appointments as completed first
        appointments = Appointment.objects.all()[:5]
        for apt in appointments:
            apt.status = 'completed'
            apt.save()
        completed_appointments = appointments
    
    payment_statuses = ['pending', 'paid', 'overdue']
    
    created_count = 0
    for appointment in completed_appointments[:8]:  # Create bills for first 8 completed appointments
        if not Billing.objects.filter(appointment=appointment).exists():
            total_amount = float(appointment.doctor.consultation_fee)
            discount = random.choice([0, 10, 20, 50])  # Random discount
            
            billing = Billing.objects.create(
                appointment=appointment,
                total_amount=total_amount,
                discount_amount=discount,
                payment_status=random.choice(payment_statuses),
                due_date=appointment.appointment_date + timedelta(days=30),
                notes=f"Consultation fee for {appointment.reason}"
            )
            
            # Set payment date for paid bills
            if billing.payment_status == 'paid':
                billing.payment_date = appointment.appointment_date + timedelta(days=random.randint(1, 7))
                billing.save()
            
            created_count += 1
    
    print(f"✓ {created_count} billing records created")

def main():
    """Main function to create all sample data"""
    print("🏥 Hospital Management System - Simple Sample Data Generator")
    print("=" * 65)
    
    try:
        print("Creating sample data...")
        create_admin()
        create_doctors()
        create_patients()
        create_appointments()
        create_billing()
        
        print()
        print("✅ Sample data creation completed successfully!")
        print()
        print("📋 Summary:")
        print(f"   • Users: {User.objects.count()}")
        print(f"   • Doctors: {Doctor.objects.count()}")
        print(f"   • Patients: {Patient.objects.count()}")
        print(f"   • Appointments: {Appointment.objects.count()}")
        print(f"   • Bills: {Billing.objects.count()}")
        print()
        print("🔐 Login Credentials:")
        print("   Admin: username='admin', password='admin123'")
        print("   Doctors: username='dr_*', password='doctor123'")
        print("   Patients: username='patient*', password='patient123'")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()