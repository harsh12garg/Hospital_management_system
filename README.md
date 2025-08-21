# Hospital Management System

A comprehensive Django-based hospital management system that streamlines healthcare operations with role-based access control for administrators, doctors, and patients.

## Features

### Core Functionality
- **Multi-role Authentication System**: Admin, Doctor, and Patient roles with tailored dashboards
- **Appointment Management**: Online booking system with conflict detection
- **Patient Records**: Comprehensive patient profiles with medical history
- **Doctor Profiles**: Detailed doctor information with specializations and availability
- **Billing System**: Automated billing with multiple payment methods
- **User Management**: Profile management with role-specific information

### Role-Based Access Control

#### Admin Features
- Complete system oversight and management
- View all patients, doctors, and appointments
- Access to billing and payment records
- User registration and role management
- System analytics and reporting

#### Doctor Features
- Personal profile and schedule management
- View assigned appointments and patient information
- Access to patient medical records
- Billing and consultation fee management
- Availability status control

#### Patient Features
- Online appointment booking with doctors
- Personal medical record management
- View appointment history and upcoming visits
- Access to billing information and payment history
- Profile management with emergency contacts

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite3 (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Forms**: Django Crispy Forms with Bootstrap 5 styling
- **Image Handling**: Pillow for profile pictures and medical images
- **Authentication**: Django's built-in authentication system

## Project Structure

```
hospital_management/
├── hospital/                    # Main application
│   ├── models.py               # Database models (User, Doctor, Patient, Appointment, Billing)
│   ├── views.py                # View controllers and business logic
│   ├── forms.py                # Django forms for user input
│   ├── urls.py                 # URL routing configuration
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── tests.py                # Unit tests
│   └── migrations/             # Database migration files
├── hospital_management/         # Project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── templates/                   # HTML templates
│   ├── hospital/               # Hospital app templates
│   │   ├── base.html           # Base template with navigation
│   │   ├── home.html           # Landing page
│   │   ├── dashboard.html      # Role-based dashboard
│   │   ├── doctors.html        # Doctor listing and search
│   │   ├── appointments.html   # Appointment management
│   │   ├── billing.html        # Billing and payments
│   │   └── profile.html        # User profile management
│   └── registration/           # Authentication templates
│       ├── login.html          # Login form
│       └── signup.html         # Registration form
├── static/                     # Static files (CSS, JS, Images)
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/                 # Static images
├── media/                      # User uploaded files
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── db.sqlite3                  # SQLite database file
```

## Database Models

### UserProfile
Extended user model with role-based access control and additional profile information.

### Doctor
- Specialization and qualifications
- Consultation fees and availability hours
- License information and experience
- Profile pictures and bio

### Patient
- Unique patient ID generation
- Medical history and allergies
- Emergency contact information
- Blood group and demographic data

### Appointment
- Doctor-patient appointment scheduling
- Conflict detection and time slot management
- Appointment types and status tracking
- Automated notifications

### Billing
- Automated billing based on consultation fees
- Multiple payment methods support
- Discount and additional charges handling
- Payment status tracking

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hospital_management
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv hospital_env
   
   # On Windows
   hospital_env\Scripts\activate
   
   # On macOS/Linux
   source hospital_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser and navigate to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage Guide

### Getting Started

1. **Admin Setup**
   - Login with superuser credentials
   - Create doctor and patient accounts through admin panel or signup
   - Configure system settings and initial data

2. **Doctor Registration**
   - Sign up with doctor role
   - Complete profile with specialization and availability
   - Set consultation fees and working hours

3. **Patient Registration**
   - Sign up with patient role
   - Complete medical profile and emergency contacts
   - Start booking appointments with available doctors

### Key Workflows

#### Appointment Booking Process
1. Patient logs in and navigates to "Book Appointment"
2. Selects preferred doctor and available time slot
3. Provides reason for consultation
4. System checks for conflicts and confirms booking
5. Automatic billing record generation

#### Doctor Schedule Management
1. Doctor updates availability hours in profile
2. Views daily and upcoming appointments in dashboard
3. Manages appointment status (completed, cancelled, etc.)
4. Accesses patient information for consultations

#### Billing and Payments
1. Automatic bill generation after appointment booking
2. Support for various payment methods
3. Discount and additional charges handling
4. Payment status tracking and overdue management

## Configuration

### Environment Variables
Create a `.env` file for production settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Email Configuration
For password reset functionality, configure email settings in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Security Features

- CSRF protection on all forms
- User authentication and session management
- Role-based access control
- SQL injection prevention through Django ORM
- XSS protection with template auto-escaping
- Secure password validation

## Testing

Run the test suite:
```bash
python manage.py test
```

For coverage reports:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up static file serving
- [ ] Configure email backend
- [ ] Set secure secret key
- [ ] Enable HTTPS
- [ ] Configure allowed hosts
- [ ] Set up backup strategy

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## API Endpoints

### Public Endpoints
- `/` - Home page
- `/about/` - About page
- `/contact/` - Contact information
- `/doctors/` - Doctor listing
- `/login/` - User authentication
- `/signup/` - User registration

### Protected Endpoints
- `/dashboard/` - Role-based dashboard
- `/appointments/` - Appointment management
- `/appointments/book/` - New appointment booking
- `/patients/` - Patient listing (admin/doctor only)
- `/billing/` - Billing records
- `/profile/` - User profile management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Ensure backward compatibility

## Troubleshooting

### Common Issues

**Database Migration Errors**
```bash
python manage.py makemigrations --empty hospital
python manage.py migrate --fake-initial
```

**Static Files Not Loading**
```bash
python manage.py collectstatic
```

**Permission Denied Errors**
- Check file permissions for media uploads
- Ensure proper directory structure exists

**Import Errors**
- Verify all dependencies are installed
- Check Python path configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check existing documentation
- Review troubleshooting section

## Changelog

### Version 1.0.0
- Initial release with core functionality
- Multi-role authentication system
- Appointment booking and management
- Billing system integration
- Responsive web interface

---

**Note**: This system is designed for educational and small-scale healthcare facilities. For production use in larger healthcare organizations, additional security measures, compliance features (HIPAA), and scalability considerations should be implemented.