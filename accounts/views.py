from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import OTP
from .serializers import OTPSerializer
from .serializers import ResetPasswordSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# for google authentication
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GenerateOTPView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []      # Disable permission

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        otp = ''.join(random.choices('0123456789', k=6))
        sender_email = "prajun0604@gmail.com"
        receiver_email = email
        password = "fgmx pzdh xnxz yojz"  # Use your app password here
        subject = "EduSphere registration One Time Password"
        body = f"OTP to register in EduSphere : {otp}"

        # Create the MIME object
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, "plain"))

        # Establish a connection to the SMTP server (in this case, Gmail)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the OTP in the database
        otp_instance = OTP.objects.create(email=email, otp=otp)
        serializer = OTPSerializer(otp_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyOTPView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []      # Disable permission

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            otp_instance = OTP.objects.get(email=email, otp=otp)
            if otp_instance.is_valid():
                otp_instance.delete()
                return Response({'message': 'OTP is valid'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = []      # Disable permission

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            try:
                # Validate the new password
                validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173/"
    client_class = OAuth2Client

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


