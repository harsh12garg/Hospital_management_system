from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile for role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"

class Doctor(models.Model):
    """Doctor model with specialization and availability"""
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('general', 'General Medicine'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='17:00')
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"
    
    def get_absolute_url(self):
        return reverse('doctor_detail', kwargs={'pk': self.pk})

class Patient(models.Model):
    """Patient model with medical information"""
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=20, unique=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.patient_id}"
    
    def get_absolute_url(self):
        return reverse('patient_detail', kwargs={'pk': self.pk})

class Appointment(models.Model):
    """Appointment booking system"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('routine', 'Routine Checkup'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=15, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.patient.user.get_full_name()} - Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"
    
    def get_absolute_url(self):
        return reverse('appointment_detail', kwargs={'pk': self.pk})

class Billing(models.Model):
    """Billing and payment records"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('insurance', 'Insurance'),
        ('online', 'Online Payment'),
    ]
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    additional_charges_description = models.TextField(blank=True)
    discount_description = models.TextField(blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bill #{self.id:05d} - {self.appointment.patient.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Calculate total amount if not set
        if not self.total_amount:
            base_amount = float(self.appointment.doctor.consultation_fee)
            self.total_amount = base_amount + float(self.additional_charges) - float(self.discount_amount)
        super().save(*args, **kwargs)