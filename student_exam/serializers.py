from rest_framework import serializers
from exam.models import Exam, Option, Question, StudentExam

class AllExamListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course_title', 'instructor_name', 'is_active', 'created_at']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'marks', 'options']

class ExamDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'instructor', 'questions']

class StudentExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExam
        fields = ['id', 'exam', 'student', 'completed', 'mark_scored']
