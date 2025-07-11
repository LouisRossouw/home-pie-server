from django.contrib import admin
from django.urls import path
# from django.views.generic.base import RedirectView
from django.urls import path, include
import main.views as main
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from user.views import CustomUserCreate, CustomTokenView


router = DefaultRouter()

urlpatterns = [
    #  path('', main.home_view, name='home'),
    path('', lambda request: redirect('admin/')),
    path('admin/', admin.site.urls),

    path('api/stats', main.stats, name='stats'),
    path('api/health', main.health, name='health'),
    path('api/test', main.test_view, name='test'),

    # User Management: Manual signup + Oauth with google
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/sign-up', CustomUserCreate.as_view(), name='user-create'),
    path('auth/login-manual', CustomTokenView.as_view(), name='login-manual'),
]
