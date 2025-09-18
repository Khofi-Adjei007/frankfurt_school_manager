# students/api/views.py
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import Talent, Sport, Student, StudentRegistrationDraft
from .serializers import TalentSerializer, SportSerializer, StudentRegistrationDraftSerializer, StudentSerializer
from ..utils import save_temp_file, move_temp_to_model_field

class TalentListAPIView(generics.ListAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer
    permission_classes = [permissions.IsAuthenticated]  # restrict as needed

class SportListAPIView(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [permissions.IsAuthenticated]

class DraftListCreateAPIView(generics.ListCreateAPIView):
    """
    Create or list drafts. Accepts multipart (files) or JSON.
    If files are present, they're saved to temp via save_temp_file and stored in uploaded_files JSON.
    """
    queryset = StudentRegistrationDraft.objects.all()
    serializer_class = StudentRegistrationDraftSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        uploaded_files = {}
        # request.FILES keys show names developer used; store mapping to temp path
        for key, f in self.request.FILES.items():
            saved = save_temp_file(f, prefix=f"draft_{key}")
            if saved:
                uploaded_files[key] = saved
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None,
                        uploaded_files=uploaded_files)

class DraftRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = StudentRegistrationDraft.objects.all()
    serializer_class = StudentRegistrationDraftSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_update(self, serializer):
        # merge provided uploaded files into existing uploaded_files map
        instance = self.get_object()
        existing = instance.uploaded_files or {}
        # save new uploaded files to temp and merge
        for key, f in self.request.FILES.items():
            saved = save_temp_file(f, prefix=f"draft_update_{key}")
            if saved:
                existing[key] = saved
        serializer.save(uploaded_files=existing)

class StudentCreateFromDraftAPIView(APIView):
    """
    POST: create final Student.
    Accept 'draft_id' to create from an existing draft (recommended).
    Alternatively accept full 'data' JSON + files (multipart).
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        draft_id = request.data.get("draft_id")
        if draft_id:
            draft = get_object_or_404(StudentRegistrationDraft, pk=draft_id, is_active=True)
            data = draft.data or {}
            files_map = draft.uploaded_files or {}
        else:
            # merge JSON payload (data) and uploaded files
            data = request.data.get("data")
            if isinstance(data, str):
                import json
                try:
                    data = json.loads(data)
                except Exception:
                    data = {}
            data = data or {}
            files_map = {}
            for key, f in request.FILES.items():
                saved = save_temp_file(f, prefix=f"submit_{key}")
                if saved:
                    files_map[key] = saved

        # Flatten merged keys if nested (depends how you stored step data). Our earlier logic expects keys used earlier.
        # For clarity assume data keys match Student model field names, or include mapping logic.

        # generate admission number
        adm_no = f"ADM{timezone.now().strftime('%Y%m%d%H%M%S')}"
        student_kwargs = {
            "admission_number": adm_no,
            "date_of_admission": data.get("date_of_admission"),
            "current_status": data.get("current_status", "ACTIVE"),
            "first_name": data.get("first_name"),
            "middle_name": data.get("middle_name"),
            "last_name": data.get("last_name"),
            "gender": data.get("gender"),
            "date_of_birth": data.get("date_of_birth"),
            "complexion": data.get("complexion"),
            "religion": data.get("religion"),
            "preferred_language": data.get("preferred_language"),
            "address": data.get("address"),
            "last_school_attended": data.get("last_school_attended"),
            "last_class_completed": data.get("last_class_completed"),
            "has_sibling_here": data.get("has_sibling_here", False),
            "sibling_name": data.get("sibling_name"),
            "sibling_class": data.get("sibling_class"),
            "blood_group": data.get("blood_group"),
            "allergies_or_conditions": data.get("allergies_or_conditions"),
            "application_number": data.get("application_number") or f"APP-{uuid4_short()}",
            "admission_approved": data.get("admission_approved", False),
            "rejection_reason": data.get("rejection_reason"),
            "class_allotted": data.get("class_allotted"),
            "remarks": data.get("remarks"),
        }

        # create student (exclude None keys if model requires)
        student = Student.objects.create(**{k:v for k,v in student_kwargs.items() if v is not None})

        # handle many-to-many fields (talents, sports) which might be lists of ids or names
        talents = data.get("talents")
        if talents:
            for t in talents:
                if isinstance(t, int):
                    try:
                        talent = Talent.objects.get(pk=t)
                        student.talents.add(talent)
                    except Talent.DoesNotExist:
                        pass
                else:
                    talent, _ = Talent.objects.get_or_create(name=t)
                    student.talents.add(talent)

        sports = data.get("sports")
        if sports:
            for s in sports:
                if isinstance(s, int):
                    try:
                        sport = Sport.objects.get(pk=s)
                        student.sports.add(sport)
                    except Sport.DoesNotExist:
                        pass
                else:
                    sport, _ = Sport.objects.get_or_create(name=s)
                    student.sports.add(sport)

        # map uploaded temp keys to student model fields (you decide mapping)
        # an example mapping — adapt to the keys you store in drafts:
        mapping = {
            "personal.photo": "photo",
            "documents.birth_certificate": "birth_certificate",
            "documents.transfer_certificate": "transfer_certificate",
            "documents.previous_academic_report": "previous_academic_report",
            "documents.passport_photo": "passport_photo",
            "documents.parent_id_proof": "parent_id_proof",
            # also allow simple keys used by stepper:
            "student_photo": "photo",
            "passport_photo": "passport_photo",
            "birth_cert": "birth_certificate",
        }

        # use files_map (either from draft.uploaded_files or from saved uploaded files)
        for key, model_field in mapping.items():
            temp_path = files_map.get(key)
            if temp_path:
                move_temp_to_model_field(student, model_field, temp_path)

        # persist student (files may have been saved with save=False)
        student.save()

        # mark draft inactive if used
        if draft_id:
            draft.is_active = False
            draft.save(update_fields=["is_active"])

        return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

# small helper used above
def uuid4_short():
    import uuid
    return uuid.uuid4().hex[:8]
