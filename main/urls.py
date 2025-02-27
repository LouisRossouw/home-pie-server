from django.contrib import admin
from django.urls import path

import main

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/stats', main.stats, name='stats'),
    path('api/health', main.health, name='health'),
]
