from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, InstructorCoursesListView, AdminCoursesListView, toggle_course_activation, AdminCoursesFullDetailView
from courses.views import CourseStudentDetailView, CourseStudentListCreateView
from courses.views import purchase_course, check_purchase_status
from courses.views import create_checkout_session, webhook, save_course
from revenue.views import InstructorRevenueView
from revenue.views import AdminRevenueView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')  # Register with basename
router.register(r'admin-details', AdminCoursesFullDetailView, basename='admin-details')  # Register with unique basename

urlpatterns = [
    path('', include(router.urls)),
    path('admin-courses/', AdminCoursesListView.as_view(), name='admin-courses-list'),
    path('instructor/<int:instructor_id>/courses/', InstructorCoursesListView.as_view(), name='instructor-courses'),
    path('courses/<int:pk>/toggle-active/', toggle_course_activation, name='toggle-course-active'),
    path('student-courses/', CourseStudentListCreateView.as_view(), name='course-list-create'),
    path('student-courses/<int:pk>/', CourseStudentDetailView.as_view(), name='course-detail'),
    path('purchase/<int:course_id>/', purchase_course, name='purchase_course'),
    path('check-purchase/<int:course_id>/', check_purchase_status, name='check_purchase_status'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('webhook/', webhook, name='webhook'),
    path('save-course/', save_course, name='save-course'),
    path('instructor/revenue/<int:instructor_id>/', InstructorRevenueView.as_view(), name='instructor-revenue'),
    path('admin/revenue/', AdminRevenueView.as_view(), name='admin-revenue'),
]
