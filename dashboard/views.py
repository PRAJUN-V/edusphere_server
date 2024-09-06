from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from decimal import Decimal
from accounts.models import Profile
from courses.models import Purchase, Course
from .serializers import AdminDashboardSerializer, CourseStatsSerializer, InstructorStatisticsSerializer, CourseSerializer
from rest_framework import status
from django.db.models.functions import ExtractDay
from django.db.models import Count
from rest_framework import generics

class AdminDashboardView(APIView):
    permission_classes = []

    def get(self, request):
        # Calculate total revenue (10% of course purchases)
        purchases = Purchase.objects.all()
        total_revenue = sum((purchase.course.price * Decimal('0.10')) for purchase in purchases)

        # Count total number of instructors
        total_instructors = Profile.objects.filter(role='instructor').count()

        # Count total number of students
        total_students = Profile.objects.filter(role='student').count()

        # Serialize the data
        data = {
            'total_revenue': total_revenue,
            'total_instructors': total_instructors,
            'total_students': total_students,
        }

        serializer = AdminDashboardSerializer(data)
        return Response(serializer.data)

class CourseStatsView(APIView):
    permission_classes = []
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseStatsSerializer(courses, many=True)
        return Response(serializer.data)

class InstructorStatisticsView(APIView):
    permission_classes = []
    def get(self, request, instructor_id):
        try:
            # Filter courses by instructor
            courses = Course.objects.filter(instructor_id=instructor_id)

            # Number of courses
            total_courses = courses.count()

            # Number of enrollments
            number_of_enrollments = Purchase.objects.filter(course__in=courses).count()

            # Number of unique students
            number_of_students = Purchase.objects.filter(course__in=courses).values('student').distinct().count()

            data = {
                'number_of_students': number_of_students,
                'number_of_enrollments': number_of_enrollments,
                'total_courses': total_courses
            }

            serializer = InstructorStatisticsSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Instructor not found'}, status=status.HTTP_404_NOT_FOUND)


class EnrollmentDataView(APIView):
    permission_classes = []
    def get(self, request, instructor_id):
        year = request.GET.get('year')
        month = request.GET.get('month')

        if not year or not month:
            return Response({'error': 'Year and month are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter purchases for the specified instructor, month, and year
        enrollments = (Purchase.objects
            .filter(course__instructor_id=instructor_id, purchase_date__year=year, purchase_date__month=month)
            .annotate(day=ExtractDay('purchase_date'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Prepare data for the chart
        data = [{'date': f"{year}-{month}-{entry['day']:02d}", 'count': entry['count']} for entry in enrollments]

        return Response(data, status=status.HTTP_200_OK)

class InstructorCoursesView(generics.GenericAPIView):
    permission_classes = []
    def get(self, request, instructor_id):
        courses = Course.objects.filter(instructor_id=instructor_id)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
