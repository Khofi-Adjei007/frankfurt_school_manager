"""Django models for Frankfurt School Manager

Refactors & improvements:
- Removes duplicate model declarations and duplicate fields.
- Adds coherent related_names and docstrings for clarity.
- Preserves existing field choices and semantics to avoid breaking changes.
- Adds helpful Meta options (ordering, indexes) where appropriate.
- Keeps production-friendly defaults (nullability, unique constraints) as provided.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------------------------------------------------------------------------
# Shared Choice Constants (kept identical to existing semantics)
# ---------------------------------------------------------------------------
POPULATION_CHOICES = [
    ("Below 100", "Below 100"),
    ("101 - 500", "101 - 500"),
    ("501 - 1000", "501 - 1000"),
    ("1001 & above", "1001 & above"),
]

USER_TYPE_CHOICES = (
    ("admin", "Admin"),
    ("teacher", "Teacher"),
    ("student", "Student"),
    ("parent", "Parent"),
)

FACILITY_NAME_CHOICES = [
    ("Borehole", "Borehole"),
    ("ICT Lab", "ICT Lab"),
    ("Library", "Library"),
    ("Science Lab", "Science Lab"),
    ("Playground", "Playground"),
    ("Dining Hall", "Dining Hall"),
]

# ---------------------------------------------------------------------------
# Reference/Lookup Models
# ---------------------------------------------------------------------------
class ExtraCurricularActivity(models.Model):
    """Lookup table for extra-curricular activities (multi-select on School)."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Extra-curricular Activity"
        verbose_name_plural = "Extra-curricular Activities"


class Talent(models.Model):
    """Lookup table for student talents/interests."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Talent"
        verbose_name_plural = "Talents"


class FacilitiesChoice(models.Model):
    """Lookup table to handle multiple facility selections for schools.

    Stored with choices to preserve your current semantics; each option
    is a unique row, which makes it easy to manage M2M relations.
    """

    name = models.CharField(max_length=50, choices=FACILITY_NAME_CHOICES, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"


# ---------------------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------------------
class School(models.Model):
    """Represents a school entity and its configuration."""

    # Basic Information
    school_name = models.CharField(max_length=255, unique=True)
    physical_address = models.CharField(max_length=255)
    digital_address = models.CharField(max_length=255)  # Ghana Post GPS code
    gps_coordinates = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Optional e.g., '5.6037° N, 0.1870° W'",
    )
    official_telephone_number = models.CharField(
        max_length=13, unique=True, blank=True, null=True,
        help_text="Include country code if applicable.",
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    website = models.URLField(blank=True, null=True)

    # Additional Information
    registration_number = models.CharField(
        max_length=50, unique=True, null=True, blank=True,
        help_text="Can be set in Setup Step 2.",
    )
    school_type = models.CharField(
        max_length=50,
        choices=[
            ("Public", "Public"),
            ("Private", "Private"),
            ("International", "International"),
            ("Mission", "Mission"),
        ],
    )
    levels = models.CharField(max_length=255, blank=True, null=True)

    # Resources (Selectable)
    population = models.CharField(
        max_length=20, choices=POPULATION_CHOICES, default="Below 100", blank=True, null=True
    )

    # Resources (Numeric)
    year_established = models.IntegerField(null=True, blank=True)
    number_of_teachers = models.PositiveIntegerField(default=0, null=True, blank=True)
    number_of_classrooms = models.PositiveIntegerField(default=0, null=True, blank=True)

    # Media
    logo = models.ImageField(upload_to="school_logos/", blank=True, null=True)

    # Governance & Identity
    board_of_directors = models.TextField(blank=True, null=True)
    motto = models.CharField(max_length=255, blank=True, null=True)

    # Many-to-many Lookups
    extra_curricular_activities = models.ManyToManyField(ExtraCurricularActivity, blank=True)
    facilities = models.ManyToManyField(FacilitiesChoice, blank=True)

    # Futuristic Hooks
    ai_analytics_enabled = models.BooleanField(default=False)
    biometric_integration = models.BooleanField(default=False)
    vr_classroom_enabled = models.BooleanField(default=False)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Principal Link (owner/admin for setup flow)
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="principal_user"
    )

    def __str__(self) -> str:
        return self.school_name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"
        ordering = ["school_name"]
        indexes = [
            models.Index(fields=["email", "registration_number"]),
        ]


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Notes:
    - Email is intentionally *not* unique. Use `username` for authentication.
    - `school` is a nullable association so users (parents/teachers/students) can be linked.
    - Custom related_names are used to avoid clashes with Django defaults.
    """

    # Personal Details
    other_names = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField()  # non-unique by design
    phone_number = models.CharField(max_length=15, null=False)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    # Role & Setup
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=None, null=True, blank=True)
    is_setup_complete = models.BooleanField(default=False)

    # School Relationship (single field, SET_NULL to prevent cascade deletes)
    school = models.ForeignKey(
        "School", on_delete=models.SET_NULL, null=True, blank=True, related_name="associated_users"
    )

    # Futuristic Hooks
    last_login_location = models.CharField(max_length=255, blank=True, null=True)
    biometric_id = models.CharField(max_length=255, blank=True, null=True)

    # Groups and Permissions (custom related_names avoid clashes)
    groups = models.ManyToManyField("auth.Group", related_name="registrations_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="registrations_user_permissions_set", blank=True
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["username"]
        indexes = [models.Index(fields=["username", "user_type"])]



