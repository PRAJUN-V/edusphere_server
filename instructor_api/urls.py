# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet
from .views import TutorPurchaseListView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('student/<int:tutor_id>/', TutorPurchaseListView.as_view(), name='tutor-purchase-list'),

]
