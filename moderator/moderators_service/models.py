from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Admin(AbstractUser):
    # Basic Information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    
    # Admin Role and Permissions
    ROLE_CHOICES = [
        ('Principal', 'Principal'),
        ('VicePrincipal', 'Vice Principal'),
        ('GeneralAdmin', 'General Admin'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    # School association (choose the one that makes sense for your use case)
    school = models.ForeignKey('gateway.School', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Permissions (defining what the admin can and cannot do)
    can_manage_timetable = models.BooleanField(default=True)
    can_manage_scheme_of_work = models.BooleanField(default=True)
    can_view_grades = models.BooleanField(default=True)
    can_edit_grades = models.BooleanField(default=False)  
    can_manage_exams = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Related fields to avoid conflicts
    groups = models.ManyToManyField(Group, related_name='admin_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='admin_permission_set', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
