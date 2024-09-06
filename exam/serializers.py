from rest_framework import serializers
from .models import Exam, Question, Option
from courses.models import Course

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['instructor', 'course', 'title']

    def create(self, validated_data):
        exam = Exam.objects.create(**validated_data)
        return exam

class QuestionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['exam', 'question_text', 'marks']

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question

class ExamListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title')

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course_title', 'is_active', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']  # Adjust fields as necessary

class ExamShowSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title')
    instructor_name = serializers.CharField(source='instructor.username')  # Adjust if you have a different field for instructor name

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course_title', 'instructor_name', 'is_active', 'created_at']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)  # Handle nested options

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'marks', 'options', 'exam']  # Include exam field

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        exam = validated_data.pop('exam')  # Ensure exam is extracted from validated_data
        question = Question.objects.create(exam=exam, **validated_data)  # Set exam field
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

class OptionShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']

class QuestionShowSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'marks', 'options']

class ExamShowsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title',  'is_active', 'created_at', 'questions']
