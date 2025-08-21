from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('doctors/', views.DoctorListView.as_view(), name='doctors'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dashboard and profile
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Appointments
    path('appointments/', views.AppointmentListView.as_view(), name='appointments'),
    path('appointments/book/', views.AppointmentCreateView.as_view(), name='book_appointment'),
    
    # Patients (admin/doctor only)
    path('patients/', views.PatientListView.as_view(), name='patients'),
    
    # Billing
    path('billing/', views.BillingListView.as_view(), name='billing'),
    
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]