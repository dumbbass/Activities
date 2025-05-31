from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    RegisterView, LoginView, ProtectedView,
    UserViewSet, ProductViewSet, OrderViewSet, PostViewSet
)
from django.shortcuts import render
from django.views.generic import TemplateView

def welcome(request):
    return render(request, 'index.html')

def index_view(request):
    return render(request, 'index.html')

def blog_view(request):
    return render(request, 'blog.html')

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('index/', index_view, name='index'),
    path('blog/', blog_view, name='blog'),
    path('rate-limit-test/', TemplateView.as_view(template_name='rate_limit_test.html'), name='rate_limit_test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 