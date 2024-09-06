from rest_framework import viewsets, permissions
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from accounts.models import Profile
from rest_framework import viewsets
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

class InstructorReviewListView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(
            role='instructor',
            admin_reviewed=False,
            application_submitted=True,
        )


class InstructorReviewDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(role='instructor')
    serializer_class = ProfileSerializer

@api_view(['POST'])
def accept_instructor(request):
    profile_id = request.data.get('instructor_id')
    profile = get_object_or_404(Profile, id=profile_id)
    profile.admin_approved = True
    profile.admin_rejected = False
    profile.admin_reviewed = True
    profile.approval_date = timezone.now()
    profile.save()

    send_mail(
        'Instructor Application Accepted',
        'Your instructor application has been accepted. You can now log in to your instructor dashboard.',
        'admin@example.com',
        [profile.user.email],
        fail_silently=False,
    )

    return JsonResponse({'message': 'Instructor accepted and email sent.'})

@api_view(['POST'])
def reject_instructor(request):
    profile_id = request.data.get('instructor_id')
    reason = request.data.get('reason')
    profile = get_object_or_404(Profile, id=profile_id)
    profile.admin_approved = False
    profile.admin_rejected = True
    profile.admin_reviewed = True
    profile.save()

    send_mail(
        'Instructor Application Rejected',
        f'Your instructor application has been rejected for the following reason: {reason}',
        'admin@example.com',
        [profile.user.email],
        fail_silently=False,
    )

    return JsonResponse({'message': 'Instructor rejected and email sent.'})

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_subcategory(self, request, pk=None):
        category = self.get_object()
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        # Filter for instructors
        return Profile.objects.filter(role='instructor')

