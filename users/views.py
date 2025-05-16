from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            if not all([username, email, password]):
                return Response(
                    {'error': 'Please provide all required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'Username already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                validate_password(password)
            except ValidationError as e:
                return Response(
                    {'error': e.messages},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not all([username, password]):
                return Response(
                    {'error': 'Please provide both username and password'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.filter(username=username).first()

            if user is None or not user.check_password(password):
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': 'This is a protected route',
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        }, status=status.HTTP_200_OK) 