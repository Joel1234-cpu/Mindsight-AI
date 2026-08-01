"""
URL configuration for mindsight project.
"""
from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/analyze/', views.analyze_message, name='analyze_message'),
    path('api/weekly-insights/', views.analyze_message, name='weekly_insights'),
]