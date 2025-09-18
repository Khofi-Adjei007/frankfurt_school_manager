from django.db import models
from django.core.exceptions import ValidationError


class AttendanceLog(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    staff = models.ForeignKey(
        "moderators.Admin",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if not self.student and not self.teacher and not self.staff:
            raise ValidationError("AttendanceLog must have at least one participant (student, teacher, or staff).")

    def __str__(self):
        if self.student:
            return f"AttendanceLog for Student {self.student.full_name}"
        elif self.teacher:
            return f"AttendanceLog for Teacher {self.teacher.full_name}"
        elif self.staff:
            return f"AttendanceLog for Staff {self.staff.full_name}"
        return "Unassigned AttendanceLog"
