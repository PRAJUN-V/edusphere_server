from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Exam, Option, Question
from .serializers import ExamSerializer, QuestionSerializer, OptionSerializer, ExamListSerializer, CourseSerializer, ExamShowSerializer, ExamShowsSerializer, QuestionAddSerializer
from rest_framework import generics
from courses.models import Course
from rest_framework.decorators import api_view

class CreateExamView(APIView):
    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateQuestionView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOptionView(APIView):
    def post(self, request):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TutorExamsView(generics.ListAPIView):
    serializer_class = ExamListSerializer

    def get_queryset(self):
        tutor_id = self.kwargs['tutor_id']
        return Exam.objects.filter(instructor_id=tutor_id)

class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        instructor_id = self.kwargs['instructor_id']
        return Course.objects.filter(instructor_id=instructor_id)

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamShowSerializer


@api_view(['POST'])
def create_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save should now include the exam field
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExamShowDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamShowsSerializer
