from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver




class User(AbstractUser):
    other_names = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='registrations_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='registrations_user_permissions_set', 
        blank=True
    )

    def __str__(self):
        return self.username


class School(models.Model):

    # Basic Information
    name = models.CharField(max_length=255)
    physical_address = models.CharField(max_length=255)
    digital_address = models.CharField(max_length=255)
    population = models.PositiveIntegerField()  
    official_telephone_number = models.CharField(max_length=13)
    year_established = models.PositiveIntegerField() 
    email = models.EmailField()
    social_media = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='school_logos/')

    # Additional Information
    registration_number = models.CharField(max_length=50, unique=True)
    principal_name = models.CharField(max_length=255) 
    board_of_directors = models.TextField(blank=True, null=True)
    motto = models.CharField(max_length=255, blank=True, null=True)
    school_type = models.CharField(max_length=50, choices=[('Public', 'Public'), ('Private', 'Private'), ('International', 'International')])
    levels = models.CharField(max_length=255, blank=True, null=True) 
    
    # School Resources
    number_of_teachers = models.PositiveIntegerField(default=0)
    number_of_classrooms = models.PositiveIntegerField(default=0)
    facilities = models.TextField(blank=True, null=True) 
    extra_curricular_activities = models.TextField(blank=True, null=True)  # Sports, clubs, etc.

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"




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
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True)
    
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




class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject_taught = models.CharField(max_length=255)
    hire_date = models.DateField()

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    grade = models.CharField(max_length=10)
    enrollment_date = models.DateField()

    def __str__(self):
        return self.user.username


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="parents")
    relation = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username



