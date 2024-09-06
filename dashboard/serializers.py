from rest_framework import serializers
from courses.models import Course, Purchase

class AdminDashboardSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_instructors = serializers.IntegerField()
    total_students = serializers.IntegerField()

class CourseStatsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    number_of_sales = serializers.SerializerMethodField()
    total_earnings = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'category', 'number_of_sales', 'total_earnings']

    def get_number_of_sales(self, obj):
        # Count the number of purchases for this course
        return Purchase.objects.filter(course=obj).count()

    def get_total_earnings(self, obj):
        # Multiply the number of purchases by the course price to get total earnings
        return Purchase.objects.filter(course=obj).count() * obj.price

class InstructorStatisticsSerializer(serializers.Serializer):
    number_of_students = serializers.IntegerField()
    number_of_enrollments = serializers.IntegerField()
    total_courses = serializers.IntegerField()

class CourseSerializer(serializers.ModelSerializer):
    number_of_students = serializers.SerializerMethodField()
    revenue = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'subtitle', 'price', 'number_of_students', 'revenue']

    def get_number_of_students(self, obj):
        return Purchase.objects.filter(course=obj).count()

    def get_revenue(self, obj):
        return Purchase.objects.filter(course=obj).count() * obj.price
