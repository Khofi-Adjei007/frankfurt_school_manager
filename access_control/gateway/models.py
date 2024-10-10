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
    registration_number = models.CharField(max_length=50)
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



