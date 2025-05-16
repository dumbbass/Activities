from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterView, LoginView, ProtectedView
from django.shortcuts import render

def welcome(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', welcome, name='welcome'),
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
] 