from rest_framework import serializers
from accounts.models import Profile
from django.contrib.auth.models import User
from accounts.models import Profile
from admin_api.models import Category
from courses.models import Purchase


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class StudentProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class HomePageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']  # We are only sending the 'name' field

class TopInstructorSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    number_of_students = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image', 'number_of_students']

    def get_profile_image(self, obj):
        # Assuming Profile model is connected to User via OneToOneField
        try:
            profile = obj.profile
            return profile.profile_image.url if profile.profile_image else None
        except Profile.DoesNotExist:
            return None

    def get_number_of_students(self, obj):
        return Purchase.objects.filter(course__instructor=obj).count()

