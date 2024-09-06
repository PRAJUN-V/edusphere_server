from rest_framework import generics
from exam.models import Exam
from .serializers import AllExamListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from exam.models import Exam, StudentExam, Option
from .serializers import ExamDetailSerializer, StudentExamSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = AllExamListSerializer

class ExamDetailView(APIView):
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        serializer = ExamDetailSerializer(exam)
        return Response(serializer.data)

    def post(self, request, exam_id):
        # Extract the student ID from the request data
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and retrieve the student
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the exam object
        exam = get_object_or_404(Exam, id=exam_id)

        # Get or create the StudentExam record
        student_exam, created = StudentExam.objects.get_or_create(student=student, exam=exam)

        if student_exam.completed:
            return Response({"detail": "You have already completed this exam."})

        # Calculate total marks
        total_marks = 0
        for question in exam.questions.all():
            selected_option_id = request.data.get(f"{question.id}")
            if selected_option_id:
                selected_option = get_object_or_404(Option, id=selected_option_id)
                if selected_option.is_correct:
                    total_marks += question.marks

        # Update the StudentExam record
        student_exam.completed = True
        student_exam.mark_scored = total_marks
        student_exam.save()

        return Response({"detail": "Exam submitted successfully.", "marks_scored": total_marks})
