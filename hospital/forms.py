from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import UserProfile, Doctor, Patient, Appointment, Billing

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, initial='patient')
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('role', css_class='form-group col-md-6 mb-3'),
                Column('phone', css_class='form-group col-md-6 mb-3'),
            ),
            'password1',
            'password2',
            Submit('submit', 'Register', css_class='btn btn-primary btn-lg w-100')
        )

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class DoctorForm(forms.ModelForm):
    """Form for doctor registration and updates"""
    class Meta:
        model = Doctor
        fields = ['specialization', 'license_number', 'experience_years', 
                 'consultation_fee', 'available_from', 'available_to', 'is_available']
        widgets = {
            'available_from': forms.TimeInput(attrs={'type': 'time'}),
            'available_to': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('specialization', css_class='form-group col-md-6 mb-3'),
                Column('license_number', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('experience_years', css_class='form-group col-md-4 mb-3'),
                Column('consultation_fee', css_class='form-group col-md-4 mb-3'),
                Column('is_available', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('available_from', css_class='form-group col-md-6 mb-3'),
                Column('available_to', css_class='form-group col-md-6 mb-3'),
            ),
            Submit('submit', 'Save Doctor Profile', css_class='btn btn-success')
        )

class PatientForm(forms.ModelForm):
    """Form for patient registration and updates"""
    class Meta:
        model = Patient
        fields = ['blood_group', 'gender', 'date_of_birth', 'emergency_contact', 'address', 'medical_history', 'allergies']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
        }

class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'appointment_type', 'reason', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'min': ''}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to today
        from datetime import date
        self.fields['appointment_date'].widget.attrs['min'] = date.today().isoformat()
        
        # Filter only available doctors
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'doctor',
            Row(
                Column('appointment_date', css_class='form-group col-md-6 mb-3'),
                Column('appointment_time', css_class='form-group col-md-6 mb-3'),
            ),
            'reason',
            Submit('submit', 'Book Appointment', css_class='btn btn-primary')
        )

class AppointmentSearchForm(forms.Form):
    """Form for searching appointments"""
    patient_name = forms.CharField(max_length=100, required=False, 
                                 widget=forms.TextInput(attrs={'placeholder': 'Patient Name'}))
    doctor_name = forms.CharField(max_length=100, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Doctor Name'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=[('', 'All Status')] + Appointment.STATUS_CHOICES, 
                              required=False)

class BillingForm(forms.ModelForm):
    """Form for creating and updating bills"""
    class Meta:
        model = Billing
        fields = ['total_amount', 'additional_charges', 'discount_amount', 
                 'payment_status', 'payment_method', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('total_amount', css_class='form-group col-md-4 mb-3'),
                Column('additional_charges', css_class='form-group col-md-4 mb-3'),
                Column('discount_amount', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('payment_status', css_class='form-group col-md-6 mb-3'),
                Column('payment_method', css_class='form-group col-md-6 mb-3'),
            ),
            'notes',
            Submit('submit', 'Save Bill', css_class='btn btn-success')
        )