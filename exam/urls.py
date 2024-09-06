from django.urls import path
from .views import CreateExamView, CreateQuestionView, CreateOptionView, TutorExamsView, CourseListView, ExamDetailView, create_question,ExamShowDetailView

urlpatterns = [
        path('create-exam/', CreateExamView.as_view(), name='create-exam'),
        path('create-question/', CreateQuestionView.as_view(), name='create-question'),
        path('create-option/', CreateOptionView.as_view(), name='create-option'),
        path('tutor/<int:tutor_id>/exams/', TutorExamsView.as_view(), name='tutor-exams'),
        path('courses/<int:instructor_id>/', CourseListView.as_view(), name='course-list'),
        path('exam/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
        path('question/', create_question, name='question-create'),
        path('exam/exam/<int:pk>/', ExamShowDetailView.as_view(), name='exam-detail'),
]
