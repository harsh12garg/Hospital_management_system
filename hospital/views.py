from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date, timedelta
from .models import Doctor, Patient, Appointment, Billing, UserProfile
from .forms import (
    CustomUserCreationForm, DoctorForm, PatientForm, AppointmentForm,
    AppointmentSearchForm, BillingForm, UserProfileForm
)

class HomeView(TemplateView):
    """Home page view"""
    template_name = 'hospital/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_doctors'] = Doctor.objects.filter(is_available=True).count()
        context['total_patients'] = Patient.objects.count()
        context['total_appointments'] = Appointment.objects.filter(
            appointment_date__gte=date.today()
        ).count()
        return context

class AboutView(TemplateView):
    """About page view"""
    template_name = 'hospital/about.html'

class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'hospital/contact.html'

def signup_view(request):
    """Custom signup view with role assignment"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone']
            )
            
            # Create role-specific profile
            if profile.role == 'doctor':
                Doctor.objects.create(
                    user=user,
                    specialization='general',
                    license_number='',
                    experience_years=0,
                    consultation_fee=500.00,
                    available_from='09:00',
                    available_to='17:00'
                )
            elif profile.role == 'patient':
                # Generate unique patient ID
                import random
                patient_id = f"PAT{random.randint(10000, 99999)}"
                Patient.objects.create(
                    user=user,
                    patient_id=patient_id
                )
            
            login(request, user)
            messages.success(request, f'Welcome {user.get_full_name()}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view with role-based content"""
    template_name = 'hospital/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            profile = user.userprofile
            context['user_role'] = profile.role
            
            if profile.role == 'patient':
                patient = Patient.objects.get(user=user)
                context['patient'] = patient
                context['upcoming_appointments'] = Appointment.objects.filter(
                    patient=patient,
                    appointment_date__gte=date.today()
                ).order_by('appointment_date', 'appointment_time')[:5]
                context['recent_bills'] = Billing.objects.filter(
                    appointment__patient=patient
                ).order_by('-created_at')[:5]
                
            elif profile.role == 'doctor':
                doctor = Doctor.objects.get(user=user)
                context['doctor'] = doctor
                context['todays_appointments'] = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=date.today()
                ).order_by('appointment_time')
                context['upcoming_appointments'] = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date__gt=date.today()
                ).order_by('appointment_date', 'appointment_time')[:5]
                
            elif profile.role == 'admin':
                context['total_doctors'] = Doctor.objects.count()
                context['total_patients'] = Patient.objects.count()
                context['total_appointments'] = Appointment.objects.count()
                context['pending_bills'] = Billing.objects.filter(payment_status='pending').count()
                
                # Recent activities
                context['recent_appointments'] = Appointment.objects.order_by('-created_at')[:5]
                context['recent_registrations'] = UserProfile.objects.order_by('-created_at')[:5]
                
        except (UserProfile.DoesNotExist, Patient.DoesNotExist, Doctor.DoesNotExist):
            context['user_role'] = 'unknown'
            
        return context

class DoctorListView(ListView):
    """List all available doctors"""
    model = Doctor
    template_name = 'hospital/doctors.html'
    context_object_name = 'doctors'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Doctor.objects.filter(is_available=True)
        specialization = self.request.GET.get('specialization')
        search = self.request.GET.get('search')
        
        if specialization:
            queryset = queryset.filter(specialization=specialization)
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(specialization__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Doctor.SPECIALIZATION_CHOICES
        context['current_specialization'] = self.request.GET.get('specialization', '')
        context['current_search'] = self.request.GET.get('search', '')
        return context

class DoctorDetailView(DetailView):
    """Doctor detail view"""
    model = Doctor
    template_name = 'hospital/doctor_detail.html'
    context_object_name = 'doctor'

class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """List all patients (admin and doctor access only)"""
    model = Patient
    template_name = 'hospital/patients.html'
    context_object_name = 'patients'
    paginate_by = 20
    
    def test_func(self):
        try:
            profile = self.request.user.userprofile
            return profile.role in ['admin', 'doctor']
        except:
            return False
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(patient_id__icontains=search)
            )
        
        return queryset

class AppointmentListView(LoginRequiredMixin, ListView):
    """List appointments based on user role"""
    model = Appointment
    template_name = 'hospital/appointments.html'
    context_object_name = 'appointments'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        try:
            profile = user.userprofile
            
            if profile.role == 'patient':
                patient = Patient.objects.get(user=user)
                queryset = Appointment.objects.filter(patient=patient)
            elif profile.role == 'doctor':
                doctor = Doctor.objects.get(user=user)
                queryset = Appointment.objects.filter(doctor=doctor)
            else:  # admin
                queryset = Appointment.objects.all()
                
        except:
            queryset = Appointment.objects.none()
        
        # Apply search filters
        form = AppointmentSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['patient_name']:
                queryset = queryset.filter(
                    Q(patient__user__first_name__icontains=form.cleaned_data['patient_name']) |
                    Q(patient__user__last_name__icontains=form.cleaned_data['patient_name'])
                )
            if form.cleaned_data['doctor_name']:
                queryset = queryset.filter(
                    Q(doctor__user__first_name__icontains=form.cleaned_data['doctor_name']) |
                    Q(doctor__user__last_name__icontains=form.cleaned_data['doctor_name'])
                )
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(appointment_date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                queryset = queryset.filter(appointment_date__lte=form.cleaned_data['date_to'])
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
        
        return queryset.order_by('-appointment_date', '-appointment_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AppointmentSearchForm(self.request.GET)
        return context

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """Create new appointment (patient only)"""
    model = Appointment
    form_class = AppointmentForm
    template_name = 'hospital/appointment_form.html'
    success_url = reverse_lazy('appointments')
    
    def form_valid(self, form):
        try:
            patient = Patient.objects.get(user=self.request.user)
            form.instance.patient = patient
            
            # Check for conflicts
            existing = Appointment.objects.filter(
                doctor=form.instance.doctor,
                appointment_date=form.instance.appointment_date,
                appointment_time=form.instance.appointment_time,
                status='scheduled'
            ).exists()
            
            if existing:
                messages.error(self.request, 'This time slot is already booked. Please choose another time.')
                return self.form_invalid(form)
            
            messages.success(self.request, 'Appointment booked successfully!')
            return super().form_valid(form)
            
        except Patient.DoesNotExist:
            messages.error(self.request, 'Only patients can book appointments.')
            return redirect('home')

class BillingListView(LoginRequiredMixin, ListView):
    """List billing records"""
    model = Billing
    template_name = 'hospital/billing.html'
    context_object_name = 'bills'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        try:
            profile = user.userprofile
            
            if profile.role == 'patient':
                patient = Patient.objects.get(user=user)
                return Billing.objects.filter(appointment__patient=patient)
            elif profile.role == 'doctor':
                doctor = Doctor.objects.get(user=user)
                return Billing.objects.filter(appointment__doctor=doctor)
            else:  # admin
                return Billing.objects.all()
                
        except:
            return Billing.objects.none()

@login_required
def profile_view(request):
    """User profile management"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        # Role-specific forms
        doctor_form = None
        patient_form = None
        
        if profile.role == 'doctor':
            try:
                doctor = Doctor.objects.get(user=request.user)
                doctor_form = DoctorForm(request.POST, instance=doctor)
            except Doctor.DoesNotExist:
                doctor_form = DoctorForm(request.POST)
                
        elif profile.role == 'patient':
            try:
                patient = Patient.objects.get(user=request.user)
                patient_form = PatientForm(request.POST, instance=patient)
            except Patient.DoesNotExist:
                patient_form = PatientForm(request.POST)
        
        # Validate and save forms
        forms_valid = [profile_form.is_valid()]
        
        if doctor_form:
            forms_valid.append(doctor_form.is_valid())
        if patient_form:
            forms_valid.append(patient_form.is_valid())
        
        if all(forms_valid):
            profile_form.save()
            
            if doctor_form:
                doctor = doctor_form.save(commit=False)
                doctor.user = request.user
                doctor.save()
                
            if patient_form:
                patient = patient_form.save(commit=False)
                patient.user = request.user
                if not patient.patient_id:
                    import random
                    patient.patient_id = f"PAT{random.randint(10000, 99999)}"
                patient.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
        doctor_form = None
        patient_form = None
        
        if profile.role == 'doctor':
            try:
                doctor = Doctor.objects.get(user=request.user)
                doctor_form = DoctorForm(instance=doctor)
            except Doctor.DoesNotExist:
                doctor_form = DoctorForm()
                
        elif profile.role == 'patient':
            try:
                patient = Patient.objects.get(user=request.user)
                patient_form = PatientForm(instance=patient)
            except Patient.DoesNotExist:
                patient_form = PatientForm()
    
    context = {
        'profile_form': profile_form,
        'doctor_form': doctor_form,
        'patient_form': patient_form,
        'user_role': profile.role,
    }
    
    return render(request, 'hospital/profile.html', context)

def logout_view(request):
    """Custom logout view that redirects to home page"""
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, f'Goodbye {user_name}! You have been logged out successfully.')
    return redirect('home')

