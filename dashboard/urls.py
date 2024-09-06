from django.urls import path
from .views import AdminDashboardView, CourseStatsView, InstructorStatisticsView, EnrollmentDataView, InstructorCoursesView

urlpatterns = [
    # for admin dashboard
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/course-stat', CourseStatsView.as_view(), name='admin-dashboard'),

    # for instructor dashboard
    path('instructor-stats/<int:instructor_id>/', InstructorStatisticsView.as_view(), name='instructor-stats'),
    path('instructor/enrollment-data/<int:instructor_id>/', EnrollmentDataView.as_view(), name='enrollment-data'),
    path('instructor-course/<int:instructor_id>/', InstructorCoursesView.as_view(), name='instructor-courses'),
]
