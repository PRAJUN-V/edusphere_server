from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet
from .views import update_user, get_user
from .views import get_student_profile, create_student_profile, update_student_profile, delete_student_profile, category_list_in_homepage, top_instructors

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/', update_user, name='update_user'),
    path('student/<int:user_id>/', get_student_profile, name='get_student_profile'),
    path('student/', create_student_profile, name='create_student_profile'),
    path('student/update/<int:user_id>/', update_student_profile, name='update_student_profile'),
    path('student/<int:user_id>/', delete_student_profile, name='delete_student_profile'),
    path('home-categories/', category_list_in_homepage, name='category-list'),
    path('top-instructors/', top_instructors, name='top-instructors'),
]
