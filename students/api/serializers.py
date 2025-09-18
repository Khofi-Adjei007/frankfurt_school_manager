# students/api/serializers.py
from rest_framework import serializers
from ..models import Student, Talent, Sport, StudentRegistrationDraft

class TalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talent
        fields = ["id", "name"]

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "name"]

class StudentRegistrationDraftSerializer(serializers.ModelSerializer):
    # data and uploaded_files are JSONFields on the model
    class Meta:
        model = StudentRegistrationDraft
        fields = ["id", "created_by", "data", "uploaded_files", "is_active", "created_at", "updated_at"]
        read_only_fields = ["created_by", "created_at", "updated_at"]

class StudentSerializer(serializers.ModelSerializer):
    talents = serializers.PrimaryKeyRelatedField(many=True, queryset=Talent.objects.all(), required=False)
    sports = serializers.PrimaryKeyRelatedField(many=True, queryset=Sport.objects.all(), required=False)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["admission_number", "date_of_admission", "created_at", "updated_at"]
