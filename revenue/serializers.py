from rest_framework import serializers
from courses.models import Course, Purchase
from django.contrib.auth.models import User
from django.db.models import Sum

class CourseRevenueSerializer(serializers.ModelSerializer):
    number_of_purchases = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'price', 'number_of_purchases', 'total_revenue']

    def get_number_of_purchases(self, obj):
        return Purchase.objects.filter(course=obj).count()

    def get_total_revenue(self, obj):
        return self.get_number_of_purchases(obj) * obj.price

class InstructorRevenueSummarySerializer(serializers.Serializer):
    instructor_id = serializers.IntegerField()
    courses = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()

    def get_courses(self, obj):
        instructor_id = obj['instructor_id']
        courses = Course.objects.filter(instructor_id=instructor_id)
        return CourseRevenueSerializer(courses, many=True).data

    def get_total_revenue(self, obj):
        instructor_id = obj['instructor_id']
        courses = Course.objects.filter(instructor_id=instructor_id)
        total_revenue = sum(course.price * Purchase.objects.filter(course=course).count() for course in courses)
        return total_revenue

class InstructorRevenueSerializer(serializers.ModelSerializer):
    instructor_username = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['instructor_username', 'total_revenue']

    def get_instructor_username(self, obj):
        return obj.username  # Get the username of the User instance

    def get_total_revenue(self, obj):
        # Calculate total revenue for the instructor
        total_revenue = Purchase.objects.filter(course__instructor=obj).aggregate(
            total_revenue=Sum('course__price')
        )['total_revenue'] or 0
        return total_revenue

