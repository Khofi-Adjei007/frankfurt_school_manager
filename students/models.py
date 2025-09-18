# students/models.py

from django.db import models
from django.conf import settings

# JSONField compatibility
try:
    JSON = models.JSONField  # Django native
except AttributeError:
    from django.contrib.postgres.fields import JSONField as JSON
    JSON = JSON

# -------------------------
# Student Registration Draft
# -------------------------
class StudentRegistrationDraft(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_registration_drafts"
    )
    data = JSON(blank=True, null=True)
    uploaded_files = JSON(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Draft #{self.pk} by {self.created_by or 'unknown'} - {self.updated_at.isoformat()}"


# -------------------------
# Choice Constants
# -------------------------
GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
COMPLEXION_CHOICES = [('FAIR', 'Fair'), ('DARK', 'Dark'), ('CHOCOLATE', 'Chocolate'), ('OLIVE', 'Olive')]
RELIGION_CHOICES = [('CHRISTIANITY', 'Christianity'), ('ISLAM', 'Islam'), ('TRADITIONAL', 'Traditional'), ('OTHER', 'Other')]
LANGUAGE_CHOICES = [('ENGLISH', 'English'), ('FRENCH', 'French'), ('SPANISH', 'Spanish'), ('OTHER', 'Other')]
ACADEMIC_STATUS_CHOICES = [('ACTIVE', 'Active'), ('ALUMNI', 'Alumni'), ('TRANSFERRED', 'Transferred'), ('SUSPENDED', 'Suspended')]
TALENT_CHOICES = [('MUSIC', 'Music'), ('DANCE', 'Dance'), ('DRAMA', 'Drama'), ('ART', 'Art'), ('DEBATE', 'Debate')]
SPORTS_CHOICES = [('FOOTBALL', 'Football'), ('BASKETBALL', 'Basketball'), ('ATHLETICS', 'Athletics'), ('VOLLEYBALL', 'Volleyball'), ('SWIMMING', 'Swimming')]


# -------------------------
# Student Model
# -------------------------
class Student(models.Model):
    # Admission Info
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_admission = models.DateField(auto_now_add=True)
    current_status = models.CharField(max_length=20, choices=ACADEMIC_STATUS_CHOICES, default='ACTIVE')

    # Personal Info
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    complexion = models.CharField(max_length=20, choices=COMPLEXION_CHOICES, blank=True, null=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True, null=True)
    preferred_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to="students/photos/", blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Education Background
    last_school_attended = models.CharField(max_length=100, blank=True, null=True)
    last_class_completed = models.CharField(max_length=50, blank=True, null=True)

    # Family Info
    has_sibling_here = models.BooleanField(default=False)
    sibling_name = models.CharField(max_length=100, blank=True, null=True)
    sibling_class = models.CharField(max_length=50, blank=True, null=True)

    # Talents & Sports
    talents = models.ManyToManyField("Talent", blank=True)
    sports = models.ManyToManyField("Sport", blank=True)

    # Medical Info
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    allergies_or_conditions = models.TextField(blank=True, null=True)

    # Documents
    birth_certificate = models.FileField(upload_to="students/docs/birthcerts/", blank=True, null=True)
    transfer_certificate = models.FileField(upload_to="students/docs/transfers/", blank=True, null=True)
    previous_academic_report = models.FileField(upload_to="students/docs/reports/", blank=True, null=True)
    passport_photo = models.ImageField(upload_to="students/docs/passports/", blank=True, null=True)
    parent_id_proof = models.FileField(upload_to="students/docs/parent_ids/", blank=True, null=True)

    # Office Use Only
    application_number = models.CharField(max_length=30, unique=True)
    admission_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    class_allotted = models.CharField(max_length=50, blank=True, null=True)
    admitted_by = models.ForeignKey(
        'moderators.Admin',  # <-- Use string reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students_admitted"
    )

    remarks = models.TextField(blank=True, null=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"


# -------------------------
# Talent & Sport Models
# -------------------------
class Talent(models.Model):
    name = models.CharField(max_length=50, choices=TALENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Sport(models.Model):
    name = models.CharField(max_length=50, choices=SPORTS_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
