# views.py
from rest_framework import viewsets
from accounts.models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated  # Ensure this import is correct

from rest_framework import generics
from rest_framework.response import Response
from courses.models import User, Purchase, Course
from .serializers import PurchaseSerializer
from django.shortcuts import get_object_or_404

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # This allows any user to access the view

class TutorPurchaseListView(generics.GenericAPIView):
    serializer_class = PurchaseSerializer

    def get(self, request, tutor_id, *args, **kwargs):
        # Get all courses taught by the tutor
        tutor = get_object_or_404(User, id=tutor_id)
        courses = Course.objects.filter(instructor=tutor)

        # Get all purchases for these courses
        purchases = Purchase.objects.filter(course__in=courses)

        # Serialize the purchase data
        serializer = self.get_serializer(purchases, many=True)
        return Response(serializer.data)
