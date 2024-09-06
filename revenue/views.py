from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InstructorRevenueSummarySerializer
from .serializers import InstructorRevenueSerializer
from django.contrib.auth.models import User
from rest_framework import status

class InstructorRevenueView(APIView):
    def get(self, request, instructor_id, *args, **kwargs):
        if not instructor_id:
            return Response({'error': 'Instructor ID is required'}, status=400)

        serializer = InstructorRevenueSummarySerializer({'instructor_id': instructor_id})
        return Response(serializer.data)

class AdminRevenueView(APIView):
    def get(self, request):
        # Retrieve all instructors who have courses
        instructors = User.objects.filter(courses__isnull=False).distinct()
        serializer = InstructorRevenueSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
