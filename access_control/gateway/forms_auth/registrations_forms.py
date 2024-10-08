from django.views.decorators.http import require_POST
from .models import School


def school_registration(request):-
    if request.method = "POST"