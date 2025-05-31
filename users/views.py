from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, Post
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, PostSerializer, RegisterSerializer
from .decorators import rate_limit

User = get_user_model()

class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @rate_limit(limit=5, period=300)  # 5 requests per 5 minutes
    def create(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @rate_limit(limit=10, period=300)  # 10 requests per 5 minutes
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
    permission_classes = [permissions.IsAuthenticated]
    
    @rate_limit(limit=60, period=60)  # 60 requests per minute
    def get(self, request):
        return Response({
            'message': 'This is a protected route',
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        }, status=status.HTTP_200_OK)

# New CRUD views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(limit=60, period=60)  # 60 requests per minute
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @rate_limit(limit=30, period=60)  # 30 requests per minute
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(limit=60, period=60)  # 60 requests per minute
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @rate_limit(limit=30, period=60)  # 30 requests per minute
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @rate_limit(limit=60, period=60)  # 60 requests per minute
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @rate_limit(limit=30, period=60)  # 30 requests per minute
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @rate_limit(limit=60, period=60)  # 60 requests per minute
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @rate_limit(limit=30, period=60)  # 30 requests per minute
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @rate_limit(limit=30, period=60)  # 30 requests per minute
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            post.likes.add(request.user)
            return Response({'status': 'liked'}) 