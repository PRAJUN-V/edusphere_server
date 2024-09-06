from accounts.models import Profile
from rest_framework import serializers
from courses.models import Course, Purchase
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle']

class StudentSerializer(serializers.ModelSerializer):
    purchased_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'purchased_courses']

class PurchaseSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    course = CourseSerializer()

    class Meta:
        model = Purchase
        fields = ['student', 'course']
