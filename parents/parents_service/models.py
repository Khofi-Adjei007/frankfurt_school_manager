from django.db import models
from django.conf import settings



PARENT_RELATION_CHOICES = [
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Guardian", "Guardian"),
    ("Other", "Other"),
]


# Create your models here.
class Parent(models.Model):
    """Parent/Guardian profile linked 1:1 with a User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_profile"
    )
    students = models.ManyToManyField("students.Student", related_name="parents")
    relation = models.CharField(max_length=50, choices=PARENT_RELATION_CHOICES)
    phone_number = models.CharField(max_length=15, null=False)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, null=False)

    # Futuristic Hook
    biometric_data = models.CharField(max_length=255, blank=True, null=True, help_text="Hashed clock-in data")

    def __str__(self) -> str:
        return f"{self.user.username} - {self.relation}"

    class Meta:
        ordering = ["user__username"]
        indexes = [models.Index(fields=["phone_number"])]
        verbose_name = "Parent"
        verbose_name_plural = "Parents"