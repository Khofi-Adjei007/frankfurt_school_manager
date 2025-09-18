from django.urls import path
from .views import (
    DraftListCreateAPIView, DraftRetrieveUpdateAPIView,
    StudentCreateFromDraftAPIView, TalentListAPIView, SportListAPIView
)

urlpatterns = [
    path("registrations/drafts/", DraftListCreateAPIView.as_view(), name="draft-list-create"),
    path("registrations/drafts/<int:pk>/", DraftRetrieveUpdateAPIView.as_view(), name="draft-detail"),
    path("registrations/submit/", StudentCreateFromDraftAPIView.as_view(), name="registration-submit"),
    path("talents/", TalentListAPIView.as_view(), name="talent-list"),
    path("sports/", SportListAPIView.as_view(), name="sport-list"),
]
