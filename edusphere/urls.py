from django.contrib import admin
from django.urls import path, include
from accounts.views import CreateUserView, GoogleLogin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomTokenObtainPairView
from accounts.views import VerifyOTPView, GenerateOTPView, ResetPasswordView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/api/user/register/", CreateUserView.as_view(), name="register"),
    path("accounts/api/token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("accounts/api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("accounts/api-auth/", include("rest_framework.urls")),

    path('admin_api/', include('admin_api.urls')),

    path('instructor/', include('instructor_api.urls')),

    path('student/', include('student_api.urls')),

    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('api/', include('api.urls')),

    path('payment/', include('payment.urls')),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('dashboard/', include('dashboard.urls')),

    path('exam/', include('exam.urls')),
    path('student-exam/', include('student_exam.urls')),

    path('chat/', include('chat.urls')),

    path('chat2/', include('chat2.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
