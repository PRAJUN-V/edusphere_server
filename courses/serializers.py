from rest_framework import serializers
from .models import Course, Purchase
from admin_api.models import Category, SubCategory
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    # instructor = UserSerializer()
    class Meta:
        model = Course
        fields = '__all__'  # or specify the fields explicitly, e.g., ['id', 'title', 'description', 'price']


class InstructorCoursesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'category', 'subcategory', 'price', 'thumbnail', 'course_video', 'description', 'what_you_will_learn', 'is_active', 'instructor']


class AdminCoursesListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = UserSerializer()
    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'category', 'subcategory', 'price', 'thumbnail', 'course_video', 'description', 'what_you_will_learn', 'is_active', 'instructor']

class AdminCoursesFullDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = UserSerializer()
    subcategory = SubCategorySerializer()
    class Meta:
        model = Course
        fields = '__all__'  # or specify the fields explicitly, e.g., ['id', 'title', 'description', 'price']


# for student course listing and doing crud operations

class SubCategoryStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CategoryStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CourseStudentSerializer(serializers.ModelSerializer):
    instructor = UserSerializer()
    category = CategorySerializer()
    subcategory = SubCategorySerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'category', 'subcategory', 'price', 'thumbnail', 'course_video', 'description', 'what_you_will_learn', 'is_active', 'instructor']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'




