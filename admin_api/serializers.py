from rest_framework import serializers
from .models import Category, SubCategory
from accounts.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'role', 'profile_image', 'profile_description',
            'github_link', 'linkedin_link', 'house_name', 'post',
            'street', 'country', 'state', 'district', 'id_proof',
            'qualification_proof', 'application_submitted', 'admin_approved',
            'admin_rejected', 'admin_reviewed', 'approval_date'
        ]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'name', 'description', 'active']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'active', 'subcategories']

