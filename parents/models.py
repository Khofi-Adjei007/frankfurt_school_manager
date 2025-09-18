from django.db import models
from django.conf import settings

PARENT_RELATION_CHOICES = [
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Guardian", "Guardian"),
    ("Other", "Other"),
]


class ParentProfile(models.Model):
    """
    Parent/Guardian profile linked 1:1 with a User.
    Supports multiple students and can store draft data for registration forms.
    """

    # Link to the single-user model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_profile"
    )

    # Many-to-many to students
    students = models.ManyToManyField(
        "students.Student",
        related_name="parents",
        blank=True
    )

    # Relation type
    relation = models.CharField(max_length=50, choices=PARENT_RELATION_CHOICES)
    phone_number = models.CharField(max_length=15)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15)

    # Optional biometric data
    biometric_data = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Hashed clock-in or biometric data"
    )

    # Draft support (for multi-step forms / registration)
    draft_data = models.JSONField(blank=True, null=True, help_text="Temporary draft data for multi-step forms")
    draft_uploaded_files = models.JSONField(blank=True, null=True, help_text="Uploaded files in draft form")

    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.relation}"

    class Meta:
        ordering = ["user__username"]
        indexes = [models.Index(fields=["phone_number"])]
        verbose_name = "Parent"
        verbose_name_plural = "Parents"
        permissions = [
            ("view_parent_profiles", "Can view parent profiles"),
            ("edit_parent_profiles", "Can edit parent profiles"),
            ("manage_student_associations", "Can manage student associations"),
        ]