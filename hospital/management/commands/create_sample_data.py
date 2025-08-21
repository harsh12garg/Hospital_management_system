from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital.models import Doctor, Patient, Appointment, Billing, UserProfile
from datetime import date, datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for testing the hospital management system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🏥 Creating sample data for Hospital Management System...'))
        
        # Create sample users
        self.create_admin()
        self.create_doctors()
        self.create_patients()
        self.create_appointments()
        self.create_billing()
        
        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully!'))
        self.stdout.write(f'📊 Summary: {User.objects.count()} users, {Doctor.objects.count()} doctors, {Patient.objects.count()} patients')

    def create_admin(self):
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
            self.stdout.write('✓ Admin user created')

    def create_doctors(self):
        doctors_data = [
            ('dr_smith', 'Sarah', 'Smith', 'cardiology', 15, 200.00),
            ('dr_johnson', 'Michael', 'Johnson', 'neurology', 12, 250.00),
            ('dr_williams', 'Emily', 'Williams', 'pediatrics', 8, 180.00),
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
                UserProfile.objects.create(user=user, role='doctor', phone=f'+1-555-010{random.randint(1,9)}')
                Doctor.objects.create(
                    user=user,
                    specialization=spec,
                    experience_years=exp,
                    consultation_fee=fee,
                    available_from='09:00',
                    available_to='17:00',
                    is_available=True
                )
                self.stdout.write(f'✓ Doctor {first_name} {last_name} created')

    def create_patients(self):
        patients_data = [
            ('patient1', 'Alice', 'Cooper', 'A+'),
            ('patient2', 'Bob', 'Wilson', 'O-'),
            ('patient3', 'Carol', 'Martinez', 'B+'),
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
                UserProfile.objects.create(user=user, role='patient', phone=f'+1-555-100{i}')
                Patient.objects.create(
                    user=user,
                    patient_id=f'PAT{10000 + i}',
                    blood_group=blood_group
                )
                self.stdout.write(f'✓ Patient {first_name} {last_name} created')

    def create_appointments(self):
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        
        for i in range(10):
            if doctors.exists() and patients.exists():
                Appointment.objects.create(
                    doctor=random.choice(doctors),
                    patient=random.choice(patients),
                    appointment_date=date.today() + timedelta(days=random.randint(1, 30)),
                    appointment_time=f'{random.randint(9, 16):02d}:00',
                    reason='Sample consultation',
                    status='scheduled'
                )
        self.stdout.write('✓ Sample appointments created')

    def create_billing(self):
        appointments = Appointment.objects.all()[:5]
        for appointment in appointments:
            if not Billing.objects.filter(appointment=appointment).exists():
                Billing.objects.create(
                    appointment=appointment,
                    total_amount=appointment.doctor.consultation_fee,
                    payment_status='pending'
                )
        self.stdout.write('✓ Sample billing records created')