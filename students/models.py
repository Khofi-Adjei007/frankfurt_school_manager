from django.db import models

# -------------------------
# Choice Constants
# -------------------------

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

COMPLEXION_CHOICES = [
    ('FAIR', 'Fair'),
    ('DARK', 'Dark'),
    ('CHOCOLATE', 'Chocolate'),
    ('OLIVE', 'Olive'),
]

RELIGION_CHOICES = [
    ('CHRISTIANITY', 'Christianity'),
    ('ISLAM', 'Islam'),
    ('TRADITIONAL', 'Traditional'),
    ('OTHER', 'Other'),
]

LANGUAGE_CHOICES = [
    ('ENGLISH', 'English'),
    ('FRENCH', 'French'),
    ('SPANISH', 'Spanish'),
    ('OTHER', 'Other'),
]

ACADEMIC_STATUS_CHOICES = [
    ('ACTIVE', 'Active'),
    ('ALUMNI', 'Alumni'),
    ('TRANSFERRED', 'Transferred'),
    ('SUSPENDED', 'Suspended'),
]

# Example talents & sports
TALENT_CHOICES = [
    ('MUSIC', 'Music'),
    ('DANCE', 'Dance'),
    ('DRAMA', 'Drama'),
    ('ART', 'Art'),
    ('DEBATE', 'Debate'),
]

SPORTS_CHOICES = [
    ('FOOTBALL', 'Football'),
    ('BASKETBALL', 'Basketball'),
    ('ATHLETICS', 'Athletics'),
    ('VOLLEYBALL', 'Volleyball'),
    ('SWIMMING', 'Swimming'),
]


class Student(models.Model):
    # -------------------------
    # Admission Info
    # -------------------------
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_admission = models.DateField(auto_now_add=True)
    current_status = models.CharField(max_length=20, choices=ACADEMIC_STATUS_CHOICES, default='ACTIVE')

    # -------------------------
    # Personal Info
    # -------------------------
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

    # -------------------------
    # Education Background
    # -------------------------
    last_school_attended = models.CharField(max_length=100, blank=True, null=True)
    last_class_completed = models.CharField(max_length=50, blank=True, null=True)

    # -------------------------
    # Family Info
    # -------------------------
    has_sibling_here = models.BooleanField(default=False)
    sibling_name = models.CharField(max_length=100, blank=True, null=True)
    sibling_class = models.CharField(max_length=50, blank=True, null=True)

    # -------------------------
    # Talents & Sports
    # -------------------------
    talents = models.ManyToManyField("Talent", blank=True)
    sports = models.ManyToManyField("Sport", blank=True)

    # -------------------------
    # Medical Info
    # -------------------------
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    allergies_or_conditions = models.TextField(blank=True, null=True)

    # -------------------------
    # Documents
    # -------------------------
    birth_certificate = models.FileField(upload_to="students/docs/birthcerts/", blank=True, null=True)
    transfer_certificate = models.FileField(upload_to="students/docs/transfers/", blank=True, null=True)
    previous_academic_report = models.FileField(upload_to="students/docs/reports/", blank=True, null=True)
    passport_photo = models.ImageField(upload_to="students/docs/passports/", blank=True, null=True)
    parent_id_proof = models.FileField(upload_to="students/docs/parent_ids/", blank=True, null=True)

    # -------------------------
    # Office Use Only
    # -------------------------
    application_number = models.CharField(max_length=30, unique=True)
    admission_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    class_allotted = models.CharField(max_length=50, blank=True, null=True)
    admitted_by = models.ForeignKey(
    "moderators_service.Admin",   # Use Admin instead of Moderator
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="students_admitted"
)



    remarks = models.TextField(blank=True, null=True)

    # -------------------------
    # System Fields
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"


class Talent(models.Model):
    name = models.CharField(max_length=50, choices=TALENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Sport(models.Model):
    name = models.CharField(max_length=50, choices=SPORTS_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
