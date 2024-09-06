from django.urls import path
from .views import ExamListCreateView, ExamDetailView

urlpatterns = [
    path('exams-list/', ExamListCreateView.as_view(), name='exam-list'),
    path('exam-details/<int:exam_id>/', ExamDetailView.as_view(), name='exam-detail'),
]
