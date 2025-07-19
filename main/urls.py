from django.contrib import admin
from django.urls import path
# from django.views.generic.base import RedirectView
from django.urls import path, include
import main.views as main
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from user.views import CustomUserCreate, CustomTokenView

from projects.time_in_progress import views as timeinprogress

router = DefaultRouter()

urlpatterns = [
    # ** Admin
    #  path('', main.home_view, name='home'),
    path('', lambda request: redirect('admin/')),
    path('admin/', admin.site.urls),

    # ** Server / API
    path('api/stats', main.stats, name='stats'),
    path('api/health', main.health, name='health'),
    path('api/test', main.test_view, name='test'),

    # ** User Management: Manual signup + Oauth with google
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/sign-up', CustomUserCreate.as_view(), name='user-create'),
    path('auth/login-manual', CustomTokenView.as_view(), name='login-manual'),

    # ** Projects
    # - TimeInProgress
    path('api/timeinprogress/overview-data', timeinprogress.overview_data, name='overview-data'),  # nopep8

]
