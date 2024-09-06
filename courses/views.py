from rest_framework import viewsets
from .models import Course, Purchase
from .serializers import CourseSerializer
from rest_framework import generics
from .serializers import InstructorCoursesSerializer, AdminCoursesListSerializer, AdminCoursesFullDetailSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CourseStudentSerializer
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
import json

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class InstructorCoursesListView(generics.ListAPIView):
    serializer_class = InstructorCoursesSerializer

    def get_queryset(self):
        instructor_id = self.kwargs['instructor_id']
        return Course.objects.filter(instructor_id=instructor_id)

class AdminCoursesListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = AdminCoursesListSerializer

@api_view(['PATCH'])
def toggle_course_activation(request, pk):
    try:
        course = Course.objects.get(pk=pk)
        course.is_active = not course.is_active
        course.save()
        return Response({'is_active': course.is_active}, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminCoursesFullDetailView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = AdminCoursesFullDetailSerializer


class CourseStudentListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseStudentSerializer

    def perform_create(self, serializer):
        serializer.save()

class CourseStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseStudentSerializer


@api_view(['POST'])
@login_required
def purchase_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        purchase, created = Purchase.objects.get_or_create(student=request.user, course=course)
        if created:
            return Response({'message': 'Course purchased successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Course already purchased'}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@login_required
def check_purchase_status(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        purchased = Purchase.objects.filter(student=request.user, course=course).exists()
        return Response({'purchased': purchased}, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_id = data.get('courseId')

            # Create a Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Course Title',  # Replace with dynamic course title
                            },
                            'unit_amount': 2000,  # Replace with dynamic course price in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'http://localhost:5173/student/course-detail/{course_id}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url='http://localhost:3000/cancel',
            )
            return JsonResponse({'id': checkout_session.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)

def handle_checkout_session(session):
    course_id = session.get('metadata', {}).get('course_id')
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
            student = User.objects.get(email=session['customer_email'])
            Purchase.objects.get_or_create(student=student, course=course)
        except Exception as e:
            print(f"Error handling checkout session: {e}")

@csrf_exempt
def save_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_id = data.get('courseId')
            user_id = data.get('userId')

            user = User.objects.get(pk=user_id)
            course = Course.objects.get(id=course_id)

            # Save purchase status
            Purchase.objects.get_or_create(student=user, course=course)

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
