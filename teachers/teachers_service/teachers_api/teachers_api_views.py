from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view(['GET'])
def teachers_service_api(request):
    data = {
        "service_name": "Teachers' Services",
        "description": "API for teachers' services"
    }
    return Response(data)
