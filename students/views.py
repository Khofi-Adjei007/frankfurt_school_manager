# students/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from .models import Student, Talent, Sport, StudentRegistrationDraft
from .utils import save_temp_file, move_temp_to_model_field, open_temp_file

# Import your step forms. Adjust paths to actual files.
from .forms.registrations.personal_info import StudentPersonalForm
from .forms.registrations.education_background import StudentEducationForm
from .forms.registrations.family_info import StudentFamilyForm
from .forms.registrations.talents_sports import StudentTalentsForm
from .forms.registrations.medical_info import StudentMedicalForm
from .forms.registrations.documents import StudentDocumentsForm
from .forms.registrations.office_use import StudentOfficeForm

SESSION_KEY = "student_registration_data"
SESSION_FILES_KEY = "student_registration_files"

class StudentRegistrationView(View):
    """
    Stepper registration view:
    - Keeps each step in session.
    - Stores uploaded files to storage (temp) and keeps paths in session.
    - Allows draft save to DB (StudentRegistrationDraft).
    - Commits atomically in final step.
    """
    FORMS = [
        ("personal", StudentPersonalForm),
        ("education", StudentEducationForm),
        ("family", StudentFamilyForm),
        ("talents", StudentTalentsForm),
        ("medical", StudentMedicalForm),
        ("documents", StudentDocumentsForm),
        ("office", StudentOfficeForm),
    ]

    def get_form(self, request, step, post=False):
        key, form_cls = self.FORMS[step]
        session_data = request.session.get(SESSION_KEY, {})
        initial = session_data.get(key, {})
        if post:
            # When called for POST we will provide data in the view.post
            return form_cls
        return form_cls(initial=initial)

    def get(self, request, step=0, draft_id=None):
        step = int(step)
        if step < 0 or step >= len(self.FORMS):
            return redirect("students:registration_step", step=0)

        # If draft_id provided, load draft into session
        if draft_id:
            draft = get_object_or_404(StudentRegistrationDraft, pk=draft_id, is_active=True)
            request.session[SESSION_KEY] = draft.data or {}
            request.session[SESSION_FILES_KEY] = draft.uploaded_files or {}
            request.session.modified = True
            messages.info(request, f"Loaded draft #{draft.pk}. You may continue.")

        form_name, form_cls = self.FORMS[step]
        form = form_cls(initial=request.session.get(SESSION_KEY, {}).get(form_name, None))
        return render(request, "students/registration_stepper.html", {
            "form": form,
            "step": step,
            "total_steps": len(self.FORMS),
            "draft_id": draft_id or "",
        })

    def post(self, request, step=0):
        step = int(step)
        if step < 0 or step >= len(self.FORMS):
            return redirect("students:registration_step", step=0)

        form_name, form_cls = self.FORMS[step]
        form = form_cls(request.POST, request.FILES)

        # Handle special action keys: back, save_draft, next
        if "back" in request.POST:
            prev_step = max(0, step - 1)
            return redirect("students:registration_step", step=prev_step)

        if "save_draft" in request.POST:
            # Validate partially (not strictly required) and persist draft
            session_data = request.session.get(SESSION_KEY, {})
            # Update current step's data if valid
            if form.is_valid():
                session_data[form_name] = form.cleaned_data
            # Save files to temp and store paths
            files_map = request.session.get(SESSION_FILES_KEY, {})
            for name, f in request.FILES.items():
                saved = save_temp_file(f, prefix=f"draft_step_{step}_{name}")
                if saved:
                    files_map[f"{form_name}.{name}"] = saved
            request.session[SESSION_KEY] = session_data
            request.session[SESSION_FILES_KEY] = files_map
            request.session.modified = True

            draft = StudentRegistrationDraft.objects.create(
                created_by=request.user if request.user.is_authenticated else None,
                data=session_data,
                uploaded_files=files_map,
            )
            messages.success(request, f"Draft saved (#{draft.pk}). You can resume later.")
            return redirect("students:registration_step", step=step)

        # Normal next-step action
        if form.is_valid():
            # Save cleaned data to session
            session_data = request.session.get(SESSION_KEY, {})
            session_data[form_name] = form.cleaned_data
            # Save uploaded files temporarily and store paths in session files map
            files_map = request.session.get(SESSION_FILES_KEY, {})
            for name, f in request.FILES.items():
                saved = save_temp_file(f, prefix=f"step_{step}_{name}")
                if saved:
                    files_map[f"{form_name}.{name}"] = saved

            request.session[SESSION_KEY] = session_data
            request.session[SESSION_FILES_KEY] = files_map
            request.session.modified = True

            # If last step -> commit atomically
            if step + 1 == len(self.FORMS):
                try:
                    with transaction.atomic():
                        student = self._create_student_from_session(request)
                        # Optionally mark any draft as inactive (if draft_id passed)
                        draft_id = request.POST.get("draft_id")
                        if draft_id:
                            StudentRegistrationDraft.objects.filter(pk=draft_id).update(is_active=False)
                except Exception as exc:
                    messages.error(request, f"Failed to create student: {exc}")
                    return render(request, "students/registration_stepper.html", {
                        "form": form,
                        "step": step,
                        "total_steps": len(self.FORMS),
                    })
                # Clear session data
                request.session.pop(SESSION_KEY, None)
                request.session.pop(SESSION_FILES_KEY, None)
                messages.success(request, f"Student {student.first_name} {student.last_name} admitted successfully.")
                return redirect("students:registration_success", pk=student.pk)

            # Not last step: redirect next
            return redirect("students:registration_step", step=step + 1)

        # invalid form — show errors on same step
        messages.error(request, "Please correct the errors below.")
        return render(request, "students/registration_stepper.html", {
            "form": form,
            "step": step,
            "total_steps": len(self.FORMS),
        })

    def _create_student_from_session(self, request):
        """
        Merge session data from all steps, create the Student instance, attach files.
        """
        session_data = request.session.get(SESSION_KEY, {})
        files_map = request.session.get(SESSION_FILES_KEY, {})

        # Merge step data dictionaries in order
        merged = {}
        for key, _ in self.FORMS:
            step_dict = session_data.get(key, {})
            if step_dict:
                merged.update(step_dict)

        # Map many-to-many fields and file fields separately
        talents_data = merged.pop("talents", None)  # form should provide list of talent names/ids
        sports_data = merged.pop("sports", None)

        # Create student core (fields that map directly to model fields)
        student = Student.objects.create(
            admission_number=merged.get("admission_number") or self._generate_admission_number(),
            date_of_admission=merged.get("date_of_admission"),
            current_status=merged.get("current_status", Student._meta.get_field("current_status").default),
            first_name=merged.get("first_name"),
            middle_name=merged.get("middle_name"),
            last_name=merged.get("last_name"),
            gender=merged.get("gender"),
            date_of_birth=merged.get("date_of_birth"),
            complexion=merged.get("complexion"),
            religion=merged.get("religion"),
            preferred_language=merged.get("preferred_language"),
            address=merged.get("address"),
            last_school_attended=merged.get("last_school_attended"),
            last_class_completed=merged.get("last_class_completed"),
            has_sibling_here=merged.get("has_sibling_here", False),
            sibling_name=merged.get("sibling_name"),
            sibling_class=merged.get("sibling_class"),
            blood_group=merged.get("blood_group"),
            allergies_or_conditions=merged.get("allergies_or_conditions"),
            application_number=merged.get("application_number") or f"APP-{student_adm_token()}",
            admission_approved=merged.get("admission_approved", False),
            rejection_reason=merged.get("rejection_reason"),
            class_allotted=merged.get("class_allotted"),
            remarks=merged.get("remarks"),
        )

        # Attach files: check for keys like "personal.photo", "documents.birth_certificate", etc.
        # Use move_temp_to_model_field helper
        mapping = {
            "personal.photo": "photo",
            "documents.birth_certificate": "birth_certificate",
            "documents.transfer_certificate": "transfer_certificate",
            "documents.previous_academic_report": "previous_academic_report",
            "documents.passport_photo": "passport_photo",
            "documents.parent_id_proof": "parent_id_proof",
        }
        for session_key, model_field in mapping.items():
            storage_path = files_map.get(session_key)
            if storage_path:
                move_temp_to_model_field(student, model_field, storage_path)

        # Save student to persist file assignments
        student.save()

        # Handle many-to-many: talents and sports.
        if talents_data:
            # talents_data can be list of IDs or names depending on forms
            for t in talents_data:
                if isinstance(t, int):
                    try:
                        talent = Talent.objects.get(pk=t)
                    except Talent.DoesNotExist:
                        continue
                else:
                    talent, _ = Talent.objects.get_or_create(name=t)
                student.talents.add(talent)
        if sports_data:
            for s in sports_data:
                if isinstance(s, int):
                    try:
                        sport = Sport.objects.get(pk=s)
                    except Sport.DoesNotExist:
                        continue
                else:
                    sport, _ = Sport.objects.get_or_create(name=s)
                student.sports.add(sport)

        student.save()
        return student

    def _generate_admission_number(self):
        """
        Simple admission number generator — replace with your school's algorithm.
        """
        from django.utils import timezone
        base = timezone.now().strftime("%Y%m%d%H%M%S")
        return f"ADM{base}"

# small helper used above for application_number fallback — replace with your own implementation
def student_adm_token():
    from random import randint
    return randint(10000, 99999)
