from django.db import models
from django.core.exceptions import ValidationError


class NotificationLog(models.Model):
    recipient_student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    recipient_parent = models.ForeignKey(
        "parents_service.Parent",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    recipient_teacher = models.ForeignKey(
        "teachers_service.Teacher",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    recipient_staff = models.ForeignKey(
        "moderators_service.Admin",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def clean(self):
        if not (self.recipient_student or self.recipient_parent or self.recipient_teacher or self.recipient_staff):
            raise ValidationError("NotificationLog must have at least one recipient.")

    def __str__(self):
        return f"Notification: {self.message[:50]}"
