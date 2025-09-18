from django.db import models
from django.conf import settings

# Create your models here.
TEACHER_QUALIFICATION_CHOICES = [
    ("Diploma", "Diploma"),
    ("Degree", "Degree"),
    ("Masters", "Masters"),
    ("Other", "Other"),
]

TEACHER_DEPARTMENT_CHOICES = [
    ("Science", "Science"),
    ("Humanities", "Humanities"),
    ("Vocational", "Vocational"),
    ("Other", "Other"),
]

# ---------------------------------------------------------------------------
# Profile Models
# ---------------------------------------------------------------------------
class Teacher(models.Model):
    """Teacher profile linked 1:1 with a User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    # Personal Details (duplicated here for fast access/display at profile level)
    other_names = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    email = models.EmailField(blank=True, null=True)

    # Teacher-Specific Details
    teacher_id = models.CharField(max_length=50, unique=True, help_text="GES registration number or internal ID")
    subject_taught = models.CharField(max_length=255)
    hire_date = models.DateField()
    qualification = models.CharField(max_length=100, choices=TEACHER_QUALIFICATION_CHOICES, default="Diploma")
    department = models.CharField(max_length=100, choices=TEACHER_DEPARTMENT_CHOICES, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, null=False)
    teaching_load = models.PositiveIntegerField(blank=True, null=True)
    certification_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Media
    photo = models.ImageField(upload_to="teacher_photos/", blank=True, null=True)

    # Futuristic Hook
    biometric_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.last_name}, {self.other_names or ''} - {self.subject_taught}"

    class Meta:
        ordering = ["last_name", "other_names"]
        indexes = [models.Index(fields=["teacher_id", "phone_number"])]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"