from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstructorReviewListView, InstructorReviewDetailView
from .views import accept_instructor, reject_instructor
from .views import CategoryViewSet, SubCategoryViewSet, ProfileViewSet

# Initialize the default router
router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'instructor-list', ProfileViewSet)

# Define the URL patterns
urlpatterns = [
    # Include the router URLs under the 'admin_api/' prefix
    path('', include(router.urls)),
    path('new_instructors/', InstructorReviewListView.as_view(), name='instructor-review-list'),
    path('instructors/<int:pk>/', InstructorReviewDetailView.as_view(), name='instructor-review-detail'),
    path('accept_instructor/', accept_instructor, name='accept_instructor'),
    path('reject_instructor/', reject_instructor, name='reject_instructor'),
    # Other paths can be added here
]
