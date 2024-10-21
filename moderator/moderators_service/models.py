from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission




class Admin(AbstractUser):
    # Basic Information
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)  # New field
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    admin_photo = models.ImageField(upload_to='admin_photos/', blank=True, null=True)  # New field
    
    # Updated Admin Role and Permissions
    ROLE_CHOICES = [
        ('Principal', 'Principal'),  # Superadmin
        ('AcademicAdmin', 'Academic Admin'),
        ('StudentServicesAdmin', 'Student Services Admin'),
        ('HRAdmin', 'Human Resource Admin'),
        ('FinanceAdmin', 'Finance Admin'),
        ('ITAdmin', 'IT Admin'),
        ('FacilitiesAdmin', 'Facilities and Operations Admin'),
        ('PRAdmin', 'Public Relations Admin'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    # School association
    school = models.ForeignKey('gateway.School', on_delete=models.SET_NULL, null=True, blank=True)

    # Permissions
    can_manage_timetable = models.BooleanField(default=True)
    can_manage_scheme_of_work = models.BooleanField(default=True)
    can_view_grades = models.BooleanField(default=True)
    can_edit_grades = models.BooleanField(default=False)
    can_manage_exams = models.BooleanField(default=False)
    can_manage_students = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)
    can_manage_finances = models.BooleanField(default=False)
    can_manage_facilities = models.BooleanField(default=False)
    can_manage_communications = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Related fields to avoid conflicts
    groups = models.ManyToManyField(Group, related_name='admin_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='admin_permission_set', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    # Assign default permissions based on role
    def assign_role_permissions(self):
        if self.role == 'Principal':
            self.can_manage_timetable = True
            self.can_manage_scheme_of_work = True
            self.can_view_grades = True
            self.can_edit_grades = True
            self.can_manage_exams = True
            self.can_manage_students = True
            self.can_manage_staff = True
            self.can_manage_finances = True
            self.can_manage_facilities = True
            self.can_manage_communications = True
        elif self.role == 'AcademicAdmin':
            self.can_manage_timetable = True
            self.can_manage_scheme_of_work = True
            self.can_view_grades = True
            self.can_edit_grades = True
            self.can_manage_exams = True
        elif self.role == 'StudentServicesAdmin':
            self.can_manage_students = True
        elif self.role == 'HRAdmin':
            self.can_manage_staff = True
        elif self.role == 'FinanceAdmin':
            self.can_manage_finances = True
        elif self.role == 'ITAdmin':
            pass  # Permissions for IT
        elif self.role == 'FacilitiesAdmin':
            self.can_manage_facilities = True
        elif self.role == 'PRAdmin':
            self.can_manage_communications = True

        self.save()

