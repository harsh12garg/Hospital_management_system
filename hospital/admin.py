from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Doctor, Patient, Appointment, Billing

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__role')
    
    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except:
            return 'No Profile'
    get_role.short_description = 'Role'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'license_number', 'consultation_fee', 'is_available')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')
    ordering = ('user__first_name',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Doctor Name'

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'patient_id', 'blood_group', 'emergency_contact')
    search_fields = ('user__first_name', 'user__last_name', 'patient_id')
    list_filter = ('blood_group',)
    ordering = ('user__first_name',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Patient Name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 
                    'doctor__user__first_name', 'doctor__user__last_name')
    date_hierarchy = 'appointment_date'
    ordering = ('-appointment_date', '-appointment_time')
    
    def get_queryset(self, request):
        # Handle cases where appointment_type field might not exist yet
        try:
            return super().get_queryset(request)
        except Exception:
            return super().get_queryset(request)
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('get_bill_id', 'get_patient_name', 'total_amount', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('appointment__patient__user__first_name', 
                    'appointment__patient__user__last_name')
    readonly_fields = ('total_amount', 'created_at')
    ordering = ('-created_at',)
    
    def get_patient_name(self, obj):
        return obj.appointment.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_bill_id(self, obj):
        return f"BILL-{obj.id:05d}"
    get_bill_id.short_description = 'Bill ID'

# Customize admin site
admin.site.site_header = "Hospital Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "Welcome to Hospital Management System"