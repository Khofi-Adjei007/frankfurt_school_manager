from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class School(models.Model):
    name = models.CharField(max_length=255)
    physical_address = models.CharField(max_length=255)
    digital_address = models.CharField(max_length=255)
    
    population = models.PositiveIntegerField()  
    official_contact = models.CharField(max_length=13)
    year_established = models.PositiveIntegerField() 
    email = models.EmailField()
    social_media = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='school_logos/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"


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


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username



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
    relation = models.CharField(max_length=50)  # e.g., Father, Mother, Guardian

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'admin':
            AdminProfile.objects.create(user=instance)
        elif instance.user_type == 'teacher':
            TeacherProfile.objects.create(user=instance)
        elif instance.user_type == 'student':
            StudentProfile.objects.create(user=instance)
        elif instance.user_type == 'parent':
            ParentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'admin':
        instance.adminprofile.save()
    elif instance.user_type == 'teacher':
        instance.teacherprofile.save()
    elif instance.user_type == 'student':
        instance.studentprofile.save()
    elif instance.user_type == 'parent':
        instance.parentprofile.save()

